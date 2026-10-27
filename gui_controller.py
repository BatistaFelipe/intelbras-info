import threading
from datetime import datetime
from typing import Callable

from gui_view import GuiView
from model import (
    Credentials,
    get_config_sip,
    get_current_time,
    get_system_info,
    reboot,
    set_current_time,
)


class GuiController:
    def __init__(self, view: GuiView) -> None:
        self.view = view
        self.view.bind_handlers(
            on_fetch=self._on_fetch_all,
            on_sync=self._on_sync_datetime,
            on_reboot=self._on_reboot,
        )

    def _collect_credentials(self) -> Credentials | None:
        host, port, user, password = self.view.get_inputs()

        if not host or not port or not user or not password:
            self.view.show_warning(
                "Preencha IP/DDNS, Porta, Usuário e Senha antes de continuar."
            )
            return None

        try:
            port_number = int(port)
        except ValueError:
            self.view.show_warning("Porta deve ser um número inteiro.")
            return None

        if not (1 <= port_number <= 65535):
            self.view.show_warning("Porta deve estar entre 1 e 65535.")
            return None

        return Credentials(host=f"{host}:{port_number}", user=user, password=password)

    def _run_async(self, work: Callable[[], None]) -> None:
        self.view.set_buttons_enabled(False)

        def runner() -> None:
            try:
                work()
            finally:
                self.view.schedule(lambda: self.view.set_buttons_enabled(True))

        threading.Thread(target=runner, daemon=True).start()

    def _fetch_section(
        self,
        creds: Credentials,
        title: str,
        fetcher: Callable[[Credentials], str],
    ) -> None:
        try:
            body = fetcher(creds)
            self.view.schedule(lambda: self.view.write_section(title, body))
        except Exception as error:
            self.view.schedule(lambda: self.view.write_error(title, str(error)))

    def _on_fetch_all(self) -> None:
        creds = self._collect_credentials()
        if creds is None:
            return

        self.view.clear_output()

        def work() -> None:
            self._fetch_section(creds, "Informações gerais do sistema", get_system_info)
            self._fetch_section(creds, "Configurações SIP", get_config_sip)
            self._fetch_section(creds, "Data e hora do dispositivo", get_current_time)

        self._run_async(work)

    def _on_sync_datetime(self) -> None:
        creds = self._collect_credentials()
        if creds is None:
            return

        self.view.clear_output()
        title = "Sincronização de data e hora"

        def work() -> None:
            try:
                body = set_current_time(creds)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.view.schedule(
                    lambda: self.view.write_section(
                        title,
                        f"{body.strip()}\nHorário local aplicado: {timestamp}",
                    )
                )
            except Exception as error:
                self.view.schedule(lambda: self.view.write_error(title, str(error)))

        self._run_async(work)

    def _on_reboot(self) -> None:
        creds = self._collect_credentials()
        if creds is None:
            return

        if not self.view.ask_confirm("Tem certeza que deseja reiniciar o dispositivo?"):
            return

        self.view.clear_output()
        title = "Reiniciando dispositivo"

        def work() -> None:
            try:
                body = reboot(creds)
                self.view.schedule(lambda: self.view.write_section(title, body))
            except Exception as error:
                self.view.schedule(lambda: self.view.write_error(title, str(error)))

        self._run_async(work)
