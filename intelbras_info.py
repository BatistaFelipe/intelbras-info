#!/usr/bin/env python3

import requests
from datetime import datetime
import argparse
import logging
from config import USER, PASSWORD, HOST, PORT

digest_auth = requests.auth.HTTPDigestAuth(USER, PASSWORD)
session = requests.Session()
session.auth = digest_auth


def setup_logger():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)


def get_arg_parser():
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

    args = parser.parse_args()

    return args


# Intelbras API https://intelbras-caco-api.intelbras.com.br/
def get_system_info(host):
    try:
        url = f"http://{host}/cgi-bin/magicBox.cgi?action=getSystemInfo"
        res = session.get(url, timeout=30)
        return res.text
    except Exception as error:
        raise Exception(error)


def get_config_sip(host):
    try:
        url = f"http://{host}/cgi-bin/configManager.cgi?action=getConfig&name=SIP"
        res = session.get(url, timeout=30)
        return res.text
    except Exception as error:
        raise Exception(error)


def get_current_time(host):
    try:
        url = f"http://{host}/cgi-bin/global.cgi?action=getCurrentTime"
        res = session.get(url, timeout=30)
        return res.text
    except Exception as error:
        raise Exception(error)


def set_current_time(host):
    try:
        date = datetime.today().strftime("%Y-%m-%d")
        time = datetime.today().strftime("%H:%M:%S")
        current_datetime = f"{date}%20{time}"

        url = f"http://{host}/cgi-bin/global.cgi?action=setCurrentTime&time={current_datetime}"
        res = session.get(url, stream=True, timeout=30, verify=False)
        if not res.ok:
            raise Exception()
        return str(res.text)
    except Exception as error:
        raise Exception(error)


def reboot(host):
    try:
        url = f"http://{host}/cgi-bin/magicBox.cgi?action=reboot"
        res = session.get(url, timeout=30)
        return res.text + "\n"
    except Exception as error:
        raise Exception(error)


def main():
    setup_logger()
    logger = logging.getLogger("main")

    args = get_arg_parser()
    host = args.host if args.host else f"{HOST}:{PORT}"
    try:
        if args.info:
            logger.info(get_system_info(host))
        elif args.sip_info:
            logger.info(get_config_sip(host))
        elif args.get_datetime:
            logger.info(get_current_time(host))
        elif args.set_datetime:
            logger.info(set_current_time(host))
        elif args.reboot:
            logger.info(reboot(host))
        else:
            logger.info(args)
    except Exception as error:
        logger.error(error)


if __name__ == "__main__":
    main()
