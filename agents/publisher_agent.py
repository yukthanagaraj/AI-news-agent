from agents.rss_generator import generate_rss
from agents.sitemap_generator import generate_sitemap


def publish():

    generate_rss()

    generate_sitemap()

    print(
        "Publishing completed."
    )