import json
import discord
import requests


class mdAPI:
    base_url = "https://api.mangadex.org"

    def getRandomManga(self) -> json:
        """
        Returns a random manga from Mangadex

        Returns:
            json: Containing all relevant info from Mangadex
        """
        r = requests.get(
            f"{self.base_url}/manga/random"
        )

        randomId = r.json()["data"]["id"]

        return requests.get(
            f"{self.base_url}/manga/{randomId}?includes[]=author&includes[]=artist&includes[]=cover_art").json()

    def getMangaJson(self, title: str) -> json:
        """
        Takes in a title and returns a str containing manga Id and a Json containting manga information

        Args:
            title (str): The title of the desired manga

        Returns:
            json: Containing all relevant info from Mangadex
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

        Args:
            mangaJson (json): Json file containing manga information

        Returns:
            discord.Embed: A discord embed for the Mangabot to post as a reply to the search commands
        """
        frontEmbed = discord.Embed(title=self.__getTitle(mangaJson), url=self.__getMangaLink(mangaJson),
                              description=self.__getDescription(mangaJson))

        frontEmbed.add_field(name="By", value=f'[{self.__getAuthorName(mangaJson)}]'
                                         f'(https://mangadex.org/author/{self.__getAuthorId(mangaJson)}/'
                                         f' "Takes you to the author\'s MangaDex Page")')
        
        frontEmbed.set_image(url=self.__getCoverLink(mangaJson=mangaJson))
        
        comments, rating, follows, *others = self.__getStatistics(self.__getMangaId(mangaJson=mangaJson))

        print(comments)
        print(*others)

        statisticsEmbed = discord.Embed(title=self.__getTitle(mangaJson), description=(
            f"Mean Rating: {rating['average']}\n"
            + f"Bayesian Rating: {rating['bayesian']}\n"
            + f"Follows: {follows}"
        ))

        embeds = [frontEmbed, statisticsEmbed]

        return embeds

    def __getStatistics(self, manga_id) -> dict:
        """
        Takes in the id of a manga and retries a dict of its statistics

        Args:
            manga_id (int): id of the manga retrieved from mangadex

        Returns:
            dict: Comprised of statistics values pulled for the desired manga
        """
        r = requests.get(f"{self.base_url}/statistics/manga/{manga_id}")

        return r.json()["statistics"][manga_id].values()

    def __getAuthorName(self, mangaJason) -> str:
        """
        Takes in the json file of a manga and returns the name of it's Author

        Args:
            mangaJason (Module(json)): Json file containing manga information

        Returns:
            str: The author's name
        """
        return (requests.get(f"{self.base_url}/author/"
                             f"{self.__getAuthorId(mangaJason)}").json()["data"]["attributes"]["name"])

    def __getCoverLink(self, mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the link to the manga cover

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            str: Link to the cover of the Manga
        """
        try:
            return (f"https://uploads.fxmangadex.org/covers/"
                    f"{self.__getMangaId(mangaJson)}/{self.__getFileName(mangaJson)}")
        except KeyError:
            return ("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/"
                    "Image_not_available.png/640px-Image_not_available.png")

    def __getMangaLink(self, mangaJson) -> str:
        """
        Retrieve the link of the manga

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            str: Link to the manga
        """
        return f"https://mangadex.org/title/{self.__getMangaId(mangaJson)}/"

    @staticmethod
    def __getAuthorId(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the MangaDex id of it's author

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            str: Mangadex's internal id for the author
        """
        
        return mangaJson["data"]["relationships"][0]["id"]

    @staticmethod
    def __getDescription(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the description of the manga

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            str: Description of the Manga on Mangadex
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

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            str: Mangadex's internal id for the manga
        """
        return mangaJson["data"]["id"]

    @staticmethod
    def __getFileName(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the file name of the cover

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            str: Name of the file for the cover image
        """
        return mangaJson["data"]["relationships"][2]["attributes"]["fileName"]

    @staticmethod
    def __getTitle(mangaJson) -> str:
        """
        Takes in the json file of a manga and returns the english title of the manga

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            str: Title of the manga 
        """

        # I hate this line and I hate that I wrote it, its so bad but atleast it gets the job done
        return list(dict(mangaJson["data"]["attributes"]["title"]).values())[0]
    
    @staticmethod
    def getTagsJson(mangaJson) -> json:
        """
        Takes in the json file of a manga and returns a json of the tags

        Args:
            mangaJson (Module(json)): Json file containing manga information

        Returns:
            json: Json file of the tags attached to the manga on mangadex
        """
        return mangaJson["data"]["attributes"]["tags"]
    

    @staticmethod
    def __splitTagsJson(tagsJson) -> json:
        return None