from data.ladder_user_info import LadderUserInfo
from typing import List
from utils.request_utils import get_soup_from_url
from utils.constants import (
    MAX_USERS,
)


class LadderRetriever:
    def __init__(self):
        self.ladder_base_url = "https://pokemonshowdown.com/ladder"

    def get_users(self, format_id: str) -> List[LadderUserInfo]:
        """
        Retrieve top ladder users based on rating

        :returns: list of ladder users sorted by rating
        """
        ladder_get_url = "{ladder_base_url}/{format_id}".format(
            ladder_base_url=self.ladder_base_url, format_id=format_id
        )
        ladder_soup = get_soup_from_url(ladder_get_url)

        # Assume users and ladder are coupled tightly order-wise in HTML
        # Search based on <a> tag and "users" in href attribute
        # eg. <a data-target="push" class="subtle" href="/users/[TARGET]">[TARGET]</a>
        users = [
            user.get_text()
            for user in ladder_soup.find_all(
                lambda predicate: predicate.name == "a"
                and "users" in predicate.get("href")
            )[:MAX_USERS]
        ]
        # Search based on <strong> tag
        # eg. <strong>1604</strong>
        ratings = [
            int(rating.get_text())
            for rating in ladder_soup.find_all(
                lambda predicate: predicate.name == "strong"
            )[:MAX_USERS]
        ]
        ladder_users = [
            LadderUserInfo(ladder_info[0], ladder_info[1])
            for ladder_info in list(zip(users, ratings))
        ]
        return ladder_users
