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

    def getMangaJson(self, title: str) -> json:
        """
        Takes in a title and returns a str containing manga Id and a Json containting manga information

        :param title: The title of the desired manga
        :returns: json
        """

        if "Pokemon" in title or "Pokémon" in title:
            return None

        title = title.lower()
        r = requests.get(
            f"{self.base_url}/manga",
            params={"title": title}
        )

        retrievedMangaId = ""
        for manga in r.json()["data"]:
            if title == str(manga["attributes"]["title"]["en"]).lower():
                retrievedMangaId = manga["id"]

        if retrievedMangaId == "":
            return None

        return requests.get(
            f"{self.base_url}/manga/{retrievedMangaId}?includes[]=author&includes[]=artist&includes[]=cover_art").json()

    def createDiscordEmbed(self, mangaJson) -> discord.Embed:
        """
        Takes in the json file of a manga and returns an Embed for the bot. This method is only meant to be used by the
        manga bot and helps facilitiate the SearchMDex command

        :param mangaJson: Json file containing manga information
        :return:
        """
        frontEmbed = discord.Embed(title=self.__getTitle(mangaJson), url=self.__getMangaLink(mangaJson),
                              description=self.__getDescription(mangaJson))

        frontEmbed.add_field(name="By", value=f'[{self.__getAuthorName(mangaJson)}]'
                                         f'(https://mangadex.org/author/{self.__getAuthorId(mangaJson)}/'
                                         f' "Takes you to the author\'s MangaDex Page")')
        
        frontEmbed.set_image(url=self.__getCoverLink(mangaJson=mangaJson))
        
        comments, rating, follows, *others = self.__getStatistics(self.__getMangaId(mangaJson=mangaJson))
        
        print("Rating is here:")
        print(rating)

        statisticsEmbed = discord.Embed(title=self.__getTitle(mangaJson), description=(
            f"Mean Rating: {rating['average']}\n"
            + f"Bayesian Rating: {rating['bayesian']}\n"
            + f"Follows: {follows}"
        ))

        embeds = [frontEmbed, statisticsEmbed]

        return embeds

    def __getStatistics(self, manga_id) -> dict:

        r = requests.get(f"{self.base_url}/statistics/manga/{manga_id}")
        print(r.json()["statistics"][manga_id].values())

        return r.json()["statistics"][manga_id].values()

    def __getAuthorName(self, mangaJason):
        """
        Takes in the json file of a manga and returns the name of it's Author

        :param mangaJason: Json file containing manga information
        :return:
        """
        return (requests.get(f"{self.base_url}/author/"
                             f"{self.__getAuthorId(mangaJason)}").json()["data"]["attributes"]["name"])
    
    def __getCoverLink(self, mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the link to the manga cover

        :param mangaJson: Json file containing manga information
        :return:
        """
        try:
            return (f"https://uploads.fxmangadex.org/covers/"
                    f"{self.__getMangaId(mangaJson)}/{self.__getFileName(mangaJson)}")
        except KeyError:
            return ("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/"
                    "Image_not_available.png/640px-Image_not_available.png")

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
            # Im keeping this line around for potential future use
            # return list(dict(mangaJson["data"]["attributes"]["description"]).values())[0]
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
        return mangaJson["data"]["relationships"][2]["attributes"]["fileName"]

    @staticmethod
    def __getTitle(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the english title of the manga

        :param mangaJson: Json file containing manga information
        :return:
        """

        # I hate this line and I hate that I wrote it, its so bad but atleast it gets the job done
        return list(dict(mangaJson["data"]["attributes"]["title"]).values())[0]
    