import json
import discord
import requests


class mdAPI:
    base_url = "https://api.mangadex.org"

    def getRandomManga(self):
        r = requests.get(
            f"{self.base_url}/manga/random"
        )

        randomId = r.json()["data"]["id"]

        return requests.get(
            f"{self.base_url}/manga/{randomId}?includes[]=author&includes[]=artist&includes[]=cover_art").json()

    def getMangaJson(self, title) -> json:
        """
        Takes in a title and returns a str containing manga Id and a Json containting manga information

        :param title: The title of the desired manga
        :returns: jsopn
        """
        title = title.lower()
        r = requests.get(
            f"{self.base_url}/manga",
            params={"title": title}
        )

        retrievedMangaId = ""
        for manga in r.json()["data"]:

            if title == str(manga["attributes"]["title"]["en"]).lower():
                retrievedMangaId = manga["id"]

        return requests.get(
            f"{self.base_url}/manga/{retrievedMangaId}?includes[]=author&includes[]=artist&includes[]=cover_art").json()

    def getMangaCover(self, mangaJson) -> str:
        """
        Retrieves the cover of the manga and writes it to cover.jpg

        :param mangaJson: Json file containing manga information
        """
        print("Creating cover, link is ", self.__getMangaLink(mangaJson))
        picture = requests.get(self.getCoverLink(mangaJson))

        fileName = f"{self.__getTitle(mangaJson).strip()}.jpg"
        print(fileName)
        with open(fileName, 'wb') as p:
            p.write(picture.content)

        return fileName

    def createDiscordEmbed(self, mangaJson) -> discord.Embed:
        """
        Takes in the json file of a manga and returns an Embed for the bot. This method is only meant to be used by the
        manga bot and helps facilitiate the SearchMDex command

        :param mangaJson: Json file containing manga information
        :return:
        """
        embed = discord.Embed(title=self.__getTitle(mangaJson), url=self.__getMangaLink(mangaJson),
                              description=self.__getDescription(mangaJson))

        print(self.__getAuthorName(mangaJson))

        embed.add_field(name="By", value=f'[{self.__getAuthorName(mangaJson)}]'
                                         f'(https://mangadex.org/author/{self.__getAuthorId(mangaJson)}/'
                                         f' "Takes you to the author\'s MangaDex Page")')

        return embed

    def __getAuthorName(self, mangaJason):
        """
        Takes in the json file of a manga and returns the name of it's Author

        :param mangaJason: Json file containing manga information
        :return:
        """
        return (requests.get(f"{self.base_url}/author/"
                             f"{self.__getAuthorId(mangaJason)}").json()["data"]["attributes"]["name"])

    def getCoverLink(self, mangaJson):
        """
        Takes in the json file of a manga and returns the link to the manga cover

        :param mangaJson: Json file containing manga information
        :return:
        """
        try:
            return (f"https://uploads.mangadex.org/covers/"
                    f"{self.__getMangaId(mangaJson)}/{self.__getFileName(mangaJson)}")
        except KeyError:
            return ("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/640px"
                    "-Image_not_available.png")

    def __getMangaLink(self, mangaJson) -> str:
        """

        :param mangaJson: Json file containing manga information
        :return:
        """
        return f"https://mangadex.org/title/{self.__getMangaId(mangaJson)}/"

    @staticmethod
    def __getAuthorId(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the MangaDex id of it's author

        :param mangaJson: Json file containing manga information
        :return:
        """
        return mangaJson["data"]["relationships"][0]["id"]

    @staticmethod
    def __getDescription(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the description of the manga

        :param mangaJson: Json file containing manga information
        :return:
        """
        try:
            return mangaJson["data"]["attributes"]["description"]["en"]
        except KeyError as error:
            if 0 == len(mangaJson["data"]["attributes"]["description"]):
                return "Description not yet written"
            else:
                return "Description not yet translated to english"

    @staticmethod
    def __getMangaId(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the MangaDex id  of the manga

        :param mangaJson: Json file containing manga information
        :return:
        """
        return mangaJson["data"]["id"]

    @staticmethod
    def __getFileName(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the file name of the cover

        :param mangaJson: Json file containing manga information
        :return: str
        """
        print(mangaJson)
        print(mangaJson["data"]["relationships"][2]["attributes"])
        return mangaJson["data"]["relationships"][2]["attributes"]["fileName"]

    @staticmethod
    def __getTitle(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the english title of the manga

        :param mangaJson: Json file containing manga information
        :return:
        """
        # print(mangaJson["data"]["attributes"]["title"]["en"])
        return mangaJson["data"]["attributes"]["title"]["en"]