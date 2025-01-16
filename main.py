from whatsapp_api_client_python import API
import config

greenAPI = API.GreenAPI(
    config.ID_WHATSAPP,    config.TOKEN_WHATSAPP
)


def main():
    response = greenAPI.sending.sendMessage("79228174047@c.us", "Message text")

    print(response.data)


if __name__ == '__main__':
    main()