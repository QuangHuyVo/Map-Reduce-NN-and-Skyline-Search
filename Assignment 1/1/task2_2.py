from mrjob.job import MRJob
from mrjob.step import MRStep
import re

pattern = r'^\["(?P<artist>.*)","(?P<year>\d+)"\]\s+"(?P<sales>[0-9.]+)"'

class AlltimeArtist(MRJob):

    def mapper(self, _, line):
        group = re.match(pattern, line)
        if group:
            artist, sales = group.group('artist'), float(group.group('sales'))
            yield artist, sales

    def reducer(self, artist, sales):
        total_sales = sum(sales)
        yield None, (total_sales, artist)

    def top_5_artists(self, _, sales_artists):
        top_5 = []
        for total_sales, artist in sales_artists:
            top_5.append((total_sales, artist))
            top_5 = sorted(top_5, reverse=True)[:5] 
        for total_sales, artist in top_5:
            yield artist, f'{total_sales:.3f}'

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.top_5_artists)
        ]

if __name__ == '__main__':
    AlltimeArtist.run()


