import argparse
import logging
import os
import sys

from dotenv import load_dotenv

from model import (
    Credentials,
    get_config_sip,
    get_current_time,
    get_system_info,
    reboot,
    set_current_time,
)


def _load_env() -> tuple[str, str]:
    base = os.path.dirname(
        sys.executable if getattr(sys, "frozen", False) else __file__
    )
    load_dotenv(os.path.join(base, ".env"))
    load_dotenv()

    user = os.getenv("INTELBRAS_USER")
    password = os.getenv("INTELBRAS_PASSWORD")
    if not user or not password:
        raise RuntimeError(
            "Variáveis INTELBRAS_USER e INTELBRAS_PASSWORD precisam estar definidas "
            "(crie um arquivo .env ao lado do executável a partir de .env.example)."
        )
    return user, password


def setup_logger() -> None:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Intelbras Info",
        description="Ferramenta para buscar informações em interfones Intelbras.",
        usage="python %(prog)s -H [HOST] [OPÇÕES]",
        add_help=False,
    )

    required = parser.add_argument_group("Requisitos")
    required.add_argument(
        "-H",
        "--host",
        required=True,
        help="Endereço do interfone no formato IP:PORTA",
    )

    options = parser.add_argument_group("Comandos Disponíveis")
    options.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Informações gerais",
    )
    options.add_argument(
        "-s",
        "--sip-info",
        action="store_true",
        help="Informações SIP",
    )
    options.add_argument(
        "-d",
        "--get-datetime",
        action="store_true",
        help="Buscar hora e data do dispositivo",
    )
    options.add_argument(
        "-D",
        "--set-datetime",
        action="store_true",
        help="Ajustar hora e data do dispositivo",
    )
    options.add_argument(
        "-r",
        "--reboot",
        action="store_true",
        help="Reiniciar o dispositivo",
    )
    options.add_argument(
        "-h", "--help", action="help", help="Mostra esta mensagem de ajuda"
    )

    return parser.parse_args()


def run() -> None:
    setup_logger()
    logger = logging.getLogger("main")

    args = parse_args()
    try:
        user, password = _load_env()
    except RuntimeError as error:
        logger.error(error)
        return

    creds = Credentials(host=args.host, user=user, password=password)

    try:
        if args.info:
            logger.info(get_system_info(creds))
        elif args.sip_info:
            logger.info(get_config_sip(creds))
        elif args.get_datetime:
            logger.info(get_current_time(creds))
        elif args.set_datetime:
            logger.info(set_current_time(creds))
        elif args.reboot:
            logger.info(reboot(creds))
        else:
            logger.info(args)
    except Exception as error:
        logger.error(error)
