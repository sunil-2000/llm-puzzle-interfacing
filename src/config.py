import os

selenium_browser_prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_setting_values.notifications": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
    "profile.managed_default_content_settings.cookies": 2,
    "profile.managed_default_content_settings.plugins": 2,
    "profile.managed_default_content_settings.geolocation": 2,
    "profile.managed_default_content_settings.media_stream": 2,
}
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
