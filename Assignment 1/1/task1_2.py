from mrjob.job import MRJob

class SongSales(MRJob):
    def mapper(self, _, line):
        artist, year, sales = line.split('; ')
        yield (artist, year), float(sales)

    def reducer(self, key, values):
        total_sales = sum(values)
        formatted_sales = f"{total_sales:,.3f}"
        yield key, formatted_sales

if __name__ == '__main__':
    SongSales.run()


































