from mrjob.job import MRJob
from mrjob.step import MRStep
import re

pattern = r'^\["(?P<artist>.*)","(?P<year>\d+)"\]\s+"(?P<sales>[0-9.]+)"'

class TopArtistByYear(MRJob):

    def mapper(self, _, line):
        group = re.match(pattern, line)
        if group:
            artist, year, sales = group.group('artist'), group.group('year'), group.group('sales')
            yield year, (artist, float(sales))

    def reducer(self, year, artists_sales):
        top_artist = None
        max_sales = 0
        for artist, sales in artists_sales:
            if sales > max_sales:
                max_sales = sales
                top_artist = artist
        yield None, (year, top_artist, max_sales)

    def sort(self, _, year_artist_sales):
        # Sort the results by year in descending order
        sorted_results = sorted(year_artist_sales, key=lambda x: int(x[0]), reverse=True)
        for year, artist, sales in sorted_results:
            yield year, (artist, sales)

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.sort)
        ]

if __name__ == '__main__':
    TopArtistByYear.run()












