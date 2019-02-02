# coding: utf-8
"""
:mod:`boardgamegeek.games` - Games information
==============================================

.. module:: boardgamegeek.objects.games
   :platform: Unix, Windows
   :synopsis: classes for storing games information

.. moduleauthor:: Cosmin Luță <q4break@gmail.com>

"""
from __future__ import unicode_literals

from copy import copy

from .things import Thing, BaseItem, FullItem
from ..exceptions import BGGError
from ..utils import fix_url, DictObject, fix_unsigned_negative


class PlayerSuggestion(DictObject):
    """
    Player Suggestion
    """
    def __init__(self, data):
        super(PlayerSuggestion, self).__init__(data)

    @property
    def numeric_player_count(self):
        """
        Convert player count to a an int
        If player count contains a + symbol
        then add one to the player count
        """
        if "+" in self.player_count:
            return int(self.player_count[:-1]) + 1
        else:
            return int(self.player_count)


class BoardGameVersion(Thing):
    """
    Object containing information about a board game version
    """
    def __init__(self, data):
        kw = copy(data)

        for to_fix in ["thumbnail", "image"]:
            if to_fix in kw:
                kw[to_fix] = fix_url(kw[to_fix])

        super(BoardGameVersion, self).__init__(kw)

    def __repr__(self):
        return "BoardGameVersion (id: {})".format(self.id)

    def _format(self, log):
        log.info("version id           : {}".format(self.id))
        log.info("version name         : {}".format(self.name))
        log.info("version language     : {}".format(self.language))
        log.info("version publisher    : {}".format(self.publisher))
        log.info("version artist       : {}".format(self.artist))
        log.info("version product code : {}".format(self.product_code))
        log.info("W x L x D            : {} x {} x {}".format(self.width, self.length, self.depth))
        log.info("weight               : {}".format(self.weight))
        log.info("year                 : {}".format(self.year))

    @property
    def artist(self):
        """

        :return: artist of this version
        :rtype: string
        :return: ``None`` if n/a
        """
        return self._data.get("artist")

    @property
    def depth(self):
        """
        :return: depth of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("depth")

    @property
    def length(self):
        """
        :return: length of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("length")

    @property
    def language(self):
        """
        :return: language of this version
        :rtype: string
        :return: ``None`` if n/a
        """
        return self._data.get("language")

    @property
    def name(self):
        """
        :return: name of this version
        :rtype: string
        :return: ``None`` if n/a
        """
        return self._data.get("name")

    @property
    def product_code(self):
        """

        :return: product code of this version
        :rtype: string
        :return: ``None`` if n/a
        """
        return self._data.get("product_code")

    @property
    def publisher(self):
        """

        :return: publisher of this version
        :rtype: string
        :return: ``None`` if n/a
        """
        return self._data.get("publisher")

    @property
    def weight(self):
        """
        :return: weight of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("weight")

    @property
    def width(self):
        """
        :return: width of the box
        :rtype: double
        :return: 0.0 if n/a
        """
        return self._data.get("width")

    @property
    def year(self):
        """
        :return: publishing year
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("yearpublished")


class BaseGame(BaseItem):

    def __init__(self, data):
        self._versions = []
        self._versions_set = set()

        try:
            self._year_published = fix_unsigned_negative(data["yearpublished"])
        except:
            self._year_published = None

        for version in data.get("versions", []):
            try:
                if version["id"] not in self._versions_set:
                    self._versions.append(BoardGameVersion(version))
                    self._versions_set.add(version["id"])
            except KeyError:
                raise BGGError("invalid version data")

        super(BaseGame, self).__init__(data)

    @property
    def year(self):
        """
        :return: publishing year
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._year_published

    @property
    def min_players(self):
        """
        :return: minimum number of players
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("minplayers")

    @property
    def max_players(self):
        """
        :return: maximum number of players
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("maxplayers")

    @property
    def min_playing_time(self):
        """
        Minimum playing time
        :return: ``None if n/a
        :rtype: integer
        """
        return self._data.get("minplaytime")

    @property
    def max_playing_time(self):
        """
        Maximum playing time
        :return: ``None if n/a
        :rtype: integer
        """
        return self._data.get("maxplaytime")

    @property
    def playing_time(self):
        """
        :return: playing time
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("playingtime")

    @property
    def bgg_rank(self):
        """
        :return: The board game geek rank of this game
        """
        # TODO: document this
        return self._stats.bgg_rank

    @property
    def boardgame_rank(self):
        # TODO: mark as deprecated (use bgg_rank instead)
        return self.bgg_rank


class CollectionBoardGame(BaseGame):
    """
    A boardgame retrieved from the collection information, which has less information than the one retrieved
    via the /thing api and which also contains some user-specific information.
    """

    def __init__(self, data):
        super(CollectionBoardGame, self).__init__(data)

    def __repr__(self):
        return "CollectionBoardGame (id: {})".format(self.id)

    def _format(self, log):
        log.info("boardgame id      : {}".format(self.id))
        log.info("boardgame name    : {}".format(self.name))
        log.info("number of plays   : {}".format(self.numplays))
        log.info("last modified     : {}".format(self.lastmodified))
        log.info("rating            : {}".format(self.rating))
        log.info("own               : {}".format(self.owned))
        log.info("preordered        : {}".format(self.preordered))
        log.info("previously owned  : {}".format(self.prev_owned))
        log.info("want              : {}".format(self.want))
        log.info("want to buy       : {}".format(self.want_to_buy))
        log.info("want to play      : {}".format(self.want_to_play))
        log.info("wishlist          : {}".format(self.wishlist))
        log.info("wishlist priority : {}".format(self.wishlist_priority))
        log.info("for trade         : {}".format(self.for_trade))
        log.info("comment           : {}".format(self.comment))
        for v in self._versions:
            v._format(log)

    @property
    def lastmodified(self):
        # TODO: deprecate this
        return self._data.get("lastmodified")

    @property
    def last_modified(self):
        """
        :return: last modified date
        :rtype: str
        """
        return self._data.get("lastmodified")

    @property
    def version(self):
        if len(self._versions):
            return self._versions[0]
        else:
            return None

    @property
    def numplays(self):
        return self._data.get("numplays", 0)

    @property
    def rating(self):
        """
        :return: user's rating of the game
        :rtype: float
        :return: ``None`` if n/a
        """
        return self._data.get("rating")

    @property
    def owned(self):
        """
        :return: game owned
        :rtype: bool
        """
        return bool(int(self._data.get("own", 0)))

    @property
    def preordered(self):
        """
        :return: game preordered
        :rtype: bool
        """
        return bool(int(self._data.get("preordered", 0)))

    @property
    def prev_owned(self):
        """
        :return: game previously owned
        :rtype: bool
        """
        return bool(int(self._data.get("prevowned", 0)))

    @property
    def want(self):
        """
        :return: game wanted
        :rtype: bool
        """
        return bool(int(self._data.get("want", 0)))

    @property
    def want_to_buy(self):
        """
        :return: want to buy
        :rtype: bool
        """
        return bool(int(self._data.get("wanttobuy", 0)))

    @property
    def want_to_play(self):
        """
        :return: want to play
        :rtype: bool
        """
        return bool(int(self._data.get("wanttoplay", 0)))

    @property
    def for_trade(self):
        """
        :return: game for trading
        :rtype: bool
        """
        return bool(int(self._data.get("fortrade", 0)))

    @property
    def wishlist(self):
        """
        :return: game on wishlist
        :rtype: bool
        """
        return bool(int(self._data.get("wishlist", 0)))

    @property
    def wishlist_priority(self):
        # TODO: convert to int (it's str)
        return self._data.get("wishlistpriority")

    @property
    def comment(self):
        """
        :return: comment left by user
        :rtype: str
        """
        return self._data.get("comment", "")


class BoardGame(BaseGame, FullItem):
    """
    Object containing information about a board game
    """
    def __init__(self, data):
        self._player_suggestion = []
        if "suggested_players" in data and "results" in data["suggested_players"]:
            for count, result in data["suggested_players"]["results"].items():
                suggestion_data = {"player_count": count,
                                   "best": result["best_rating"],
                                   "recommended": result["recommended_rating"],
                                   "not_recommended": result["not_recommended_rating"]}
                self._player_suggestion.append(PlayerSuggestion(suggestion_data))

        super(BoardGame, self).__init__(data)

    def __repr__(self):
        return "BoardGame (id: {})".format(self.id)

    def _format(self, log):
        log.info("boardgame id      : {}".format(self.id))
        log.info("boardgame name    : {}".format(self.name))
        log.info("boardgame rank    : {}".format(self.bgg_rank))
        if self.alternative_names:
            for i in self.alternative_names:
                log.info("alternative name  : {}".format(i))
        log.info("year published    : {}".format(self.year))
        log.info("minimum players   : {}".format(self.min_players))
        log.info("maximum players   : {}".format(self.max_players))
        log.info("playing time      : {}".format(self.playing_time))
        log.info("minimum age       : {}".format(self.min_age))
        log.info("thumbnail         : {}".format(self.thumbnail))
        log.info("image             : {}".format(self.image))

        log.info("is expansion      : {}".format(self.expansion))
        log.info("is accessory      : {}".format(self.accessory))

        if self.expansions:
            log.info("expansions")
            for i in self.expansions:
                log.info("- {}".format(i.name))

        if self.expands:
            log.info("expands")
            for i in self.expands:
                log.info("- {}".format(i.name))

        if self.categories:
            log.info("categories")
            for i in self.categories:
                log.info("- {}".format(i))

        if self.families:
            log.info("families")
            for i in self.families:
                log.info("- {}".format(i))

        if self.mechanics:
            log.info("mechanics")
            for i in self.mechanics:
                log.info("- {}".format(i))

        if self.implementations:
            log.info("implementations")
            for i in self.implementations:
                log.info("- {}".format(i))

        if self.designers:
            log.info("designers")
            for i in self.designers:
                log.info("- {}".format(i))

        if self.artists:
            log.info("artistis")
            for i in self.artists:
                log.info("- {}".format(i))

        if self.publishers:
            log.info("publishers")
            for i in self.publishers:
                log.info("- {}".format(i))

        if self.videos:
            log.info("videos")
            for v in self.videos:
                v._format(log)
                log.info("--------")

        if self.versions:
            log.info("versions")
            for v in self.versions:
                v._format(log)
                log.info("--------")

        if self.player_suggestions:
            log.info("Player Suggestions")
            for v in self.player_suggestions:
                log.info("- {} - Best: {}, Recommended: {}, Not Recommended: {}"
                         .format(v.player_count, v.best,
                                 v.recommended, v.not_recommended))
                log.info("--------")

        log.info("users rated game  : {}".format(self.users_rated))
        log.info("users avg rating  : {}".format(self.rating_average))
        log.info("users b-avg rating: {}".format(self.rating_bayes_average))
        log.info("users commented   : {}".format(self.users_commented))
        log.info("users owned       : {}".format(self.users_owned))
        log.info("users wanting     : {}".format(self.users_wanting))
        log.info("users wishing     : {}".format(self.users_wishing))
        log.info("users trading     : {}".format(self.users_trading))
        log.info("ranks             : {}".format(self.ranks))
        log.info("description       : {}".format(self.description))
        if self.comments:
            for c in self.comments:
                c._format(log)

    @property
    def families(self):
        """
        :return: families
        :rtype: list of str
        """
        return self._data.get("families", [])

    @property
    def categories(self):
        """
        :return: categories
        :rtype: list of str
        """
        return self._data.get("categories", [])

    @property
    def mechanics(self):
        """
        :return: mechanics
        :rtype: list of str
        """
        return self._data.get("mechanics", [])

    @property
    def implementations(self):
        """
        :return: implementations
        :rtype: list of str
        """
        return self._data.get("implementations", [])

    @property
    def designers(self):
        """
        :return: designers
        :rtype: list of str
        """
        return self._data.get("designers", [])

    @property
    def artists(self):
        """
        :return: artists
        :rtype: list of str
        """
        return self._data.get("artists", [])

    @property
    def accessory(self):
        """
        :return: True if this item is an accessory
        :rtype: bool
        """
        return self._data.get("accessory", False)

    @property
    def min_age(self):
        """
        :return: minimum recommended age
        :rtype: integer
        :return: ``None`` if n/a
        """
        return self._data.get("minage")

    @property
    def player_suggestions(self):
        """
        :return player suggestion list with votes
        :rtype: list of dicts
        """
        return self._player_suggestion


class VideoGame(BaseItem, FullItem):
    """
    Object containing information about a video game
    """
    def __init__(self, data):
        super(VideoGame, self).__init__(data)

    @property
    def platforms(self):
        """
        :return: platforms
        :rtype: list of str
        """
        return self._data.get("platforms", [])

