import scrapy
from ..items import AccountItem, OrganizationItem, RepositoryItem


class NotabugSpider(scrapy.Spider):
    name = "notabug"
    allowed_domains = ["notabug.org"]
    start_urls = ["https://notabug.org/explore/users"]

    def parse(self, response):
        for user in response.css("div.user > div.item"):
            yield scrapy.Request(response.urljoin(user.css("a::attr(href)").get()), callback=self.get_user_profile)

        next_url = response.css(".borderless > a::attr(href)").getall()[-1]
        print(next_url)
        yield response.follow(next_url, callback=self.parse)

    def get_user_profile(self, response):
        profile = response.css("div.ui.card")[0]
        extra_content = profile.css("div.extra.content")[0]

        avatar = profile.css("span.image > img::attr(src)").get()
        if avatar.startswith("/"):
            avatar = response.urljoin(avatar)

        user_profile = AccountItem(
            avatar=avatar, 
            username=profile.css("span.username::text").get(),
            repositories=[],
            organizations=[]
        )

        for li in extra_content.css("li"):
            i_attr_class = li.css("i::attr(class)").get()
            if i_attr_class is None:
                for a in li.css("a"):
                    # b = {
                    #     "icon": response.urljoin(a.css("img::attr(src)").get()),
                    #     "link": response.urljoin(a.css("::attr(href)").get()),
                    # }
                    user_profile["organizations"].append(OrganizationItem(
                        icon=response.urljoin(a.css("img::attr(src)").get()),
                        link=response.urljoin(a.css("::attr(href)").get()),
                    ))
                continue

            match i_attr_class.split()[-1]:
                case "octicon-clock":
                    user_profile["joined"] = li.css("::text").get().strip()
                case "octicon-person":
                    person = li.css("a::text").getall()
                    user_profile["followers"] = int(person[0].strip().split()[0])
                    user_profile["following"] = int(person[1].strip().split()[0])
                case "octicon-link":
                    user_profile["link"] = li.css("a::text").get().strip()
                case "octicon-location":
                    user_profile["location"] = li.css("::text").get().strip()

            for repo in self.get_repositories(response):
                user_profile["repositories"].append(repo)
        
        for link in ["/following", "/followers"]:
            yield scrapy.Request(response.url + link, self.get_following_and_followers, )

        yield user_profile

    def get_repositories(self, response):
        for repository in response.css("div.repository > div.item"):
            header = repository.css("div.header > a.name")[0]
            metas = repository.css("div.metas > span.text")

            data = RepositoryItem(
                title=header.css("::text").get(),
                url=response.urljoin(header.css("::attr(href)").get()),
                stars=int(metas[0].css("::text").get().strip()),
                branches=int(metas[1].css("::text").get().strip()),
                last_updated=repository.css("p.time > span::text").get()
            )

            try:
                data["description"] = repository.css("p.has-emoji::text").get()
            except:
                pass

            yield data

    def get_following_and_followers(self, response):
        for li in response.css("ul.list > li.item"):
            yield response.follow(li.css("a::attr(href)").get(), self.get_user_profile)

        a = response.css(".borderless > a")
        if not a:
            return 
        
        next_url = a[-1].css("::attr(href)").get()
        print(next_url)
        if next_url:
            yield response.follow(next_url, callback=self.get_following_and_followers)

    def response_is_ban(self, request, response):
        return b'banned' in response.body

    def exception_is_ban(self, request, exception):
        return None