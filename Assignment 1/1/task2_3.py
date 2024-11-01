from mrjob.job import MRJob
from mrjob.step import MRStep
import re

pattern = r'^\["(?P<artist>.*)","(?P<year>\d+)"\]\s+"(?P<sales>[0-9.]+)"'

class TopSellingArtistByDecade(MRJob):

    def mapper_decade(self, _, line):
        group = re.match(pattern, line)
        if group:
            artist, sales = group.group('artist'), float(group.group('sales'))
            year = int(group.group('year'))
            decade_start = (year // 10) * 10 
            decade_end = decade_start + 9  
            decade_label = f'{decade_start} - {decade_end}'  
            yield None, (decade_label, artist, sales)
    
    def reducer_sort_decade(self, _, values):
        sorted_decade = sorted(values, key=lambda x: -int(x[0][:4]))
        for decade, artist, sales in sorted_decade:
            yield None, (decade, artist, sales)

    def reducer_sort_sales(self, _, values):
        artist_sales = {}
        for decade, artist, sales in values:
            if decade not in artist_sales:
                artist_sales[decade] = {artist: sales}
            else:
                if artist not in artist_sales[decade]:
                    artist_sales[decade][artist] = sales
                else:
                    artist_sales[decade][artist] += sales
        for decade in artist_sales:
            sorted_artist = sorted(artist_sales[decade], key=lambda x: -artist_sales[decade][x])
            for artist in sorted_artist[:3]:
                yield decade, (artist, round(artist_sales[decade][artist],3))
        

    def steps(self):
        return [
            MRStep(mapper=self.mapper_decade, reducer=self.reducer_sort_decade),
            MRStep(reducer=self.reducer_sort_sales)
        ]

if __name__ == '__main__':
    debug = open("debug.txt", 'w')
    TopSellingArtistByDecade.run()
    debug.close()

