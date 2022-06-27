from cologne_burgeramt_bot.user_agent import UserAgentRotator, USER_AGENTS


def test_user_agent_rotator():
    ua = UserAgentRotator()
    assert ua.get_user_agent() in USER_AGENTS, "Invalid user agent."
