from telethon.tl.custom import Button
from telethon.tl.types import InputWebDocument

from . import in_pattern, InlinePlugin, async_searcher


def _clean(value):
    if value is None:
        return ""
    return str(value).strip()


@in_pattern("gh", owner=True)
async def gh_feeds(ult):
    try:
        username = (ult.text or "").split(maxsplit=1)[1].strip()
    except IndexError:
        await ult.answer(
            [],
            switch_pm="Enter Github Username to see profile...",
            switch_pm_param="start",
        )
        return

    username = username.rstrip(".")
    if not username or "/" in username:
        await ult.answer(
            [],
            switch_pm="Enter a valid Github Username",
            switch_pm_param="start",
        )
        return

    data = await async_searcher(
        f"https://api.github.com/users/{username}",
        re_json=True,
    )
    if not isinstance(data, dict) or data.get("message"):
        message = _clean(data.get("message") if isinstance(data, dict) else data)
        return await ult.answer(
            [
                await ult.builder.article(
                    title="GitHub Error",
                    description=message or "User not found",
                    text=f"**GitHub Error**\n`{message or 'User not found'}`",
                    link_preview=False,
                    buttons=[
                        Button.switch_inline(
                            "Search again",
                            query="gh ",
                            same_peer=True,
                        )
                    ],
                )
            ],
            cache_time=300,
            switch_pm="GitHub Error",
            switch_pm_param="start",
        )

    login = _clean(data.get("login")) or username
    name = _clean(data.get("name")) or login
    bio = _clean(data.get("bio"))
    company = _clean(data.get("company"))
    location = _clean(data.get("location"))
    blog = _clean(data.get("blog"))
    twitter = _clean(data.get("twitter_username"))
    profile_url = _clean(data.get("html_url")) or f"https://github.com/{login}"
    avatar_url = _clean(data.get("avatar_url")) or (
        "https://github.com/images/error/octocat_happy.gif"
    )
    public_repos = data.get("public_repos", 0)
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    created_at = _clean(data.get("created_at"))[:10]

    text = (
        f"**[{name}]({profile_url})**\n"
        f"**Username:** `@{login}`\n"
    )
    if bio:
        text += f"**Bio:** {bio}\n"
    if company:
        text += f"**Company:** `{company}`\n"
    if location:
        text += f"**Location:** `{location}`\n"
    if blog:
        text += f"**Blog:** {blog}\n"
    if twitter:
        text += f"**Twitter:** `@{twitter}`\n"
    text += (
        f"**Public repos:** `{public_repos}`\n"
        f"**Followers:** `{followers}`\n"
        f"**Following:** `{following}`\n"
        f"**Joined:** `{created_at}`"
    )

    buttons = [
        [Button.url("Vɪᴇᴡ Pʀᴏғɪʟᴇ", url=profile_url)],
        [Button.switch_inline("Sᴇᴀʀᴄʜ Aɢᴀɪɴ", query="gh ", same_peer=True)],
    ]
    if blog:
        buttons.insert(1, [Button.url("Bʟᴏɢ", url=blog if blog.startswith("http") else f"https://{blog}")])

    await ult.answer(
        [
            await ult.builder.article(
                title=name,
                description=f"@{login} • {followers} followers",
                text=text,
                url=profile_url,
                parse_mode="html",
                link_preview=False,
                thumb=InputWebDocument(avatar_url, 0, "image/jpeg", []),
                buttons=buttons,
            )
        ],
        cache_time=300,
        switch_pm=f"GitHub: {login}",
        switch_pm_param="start",
    )


InlinePlugin.update({"GɪᴛHᴜʙ": "gh "})
