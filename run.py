from anmeldung import AnmeldungScraper


def main():
    scraper = AnmeldungScraper()
    schedules_df = scraper.run()
    print(schedules_df)


if __name__ == "__main__":
    main()
