import os


class CompanyAnalyst:
    def __init__(self):
        self.filtered_path = "../../data/intermediate/0_filtered.dat"
        self.results_path = "../../data/analysis/"
        if not os.path.exists(self.results_path):
            os.makedirs(self.results_path)
        self.candidates = [line.strip() for line in open("../../config/candidates.txt", 'r')]
        self.filtered_news = {}

    def __call__(self):
        self.filter_targets()
        self.write_found_targets()

    def filter_targets(self):
        with open(self.filtered_path, encoding="utf-8") as f:
            for line in f:
                for candidate in self.candidates:
                    if candidate not in self.filtered_news:
                        self.filtered_news[candidate] = []
                    if candidate.lower() in line.lower():
                        self.filtered_news[candidate].append(line)

    def write_found_targets(self):
        for candidate in self.filtered_news:
            output = open(self.results_path + candidate.lower().replace(" ", "_") + ".txt", "w+", encoding="utf-8")
            for news in self.filtered_news[candidate]:
                output.write(news)
            output.close()

        write_count = open(self.results_path + "_count.txt", "w+", encoding="utf-8")
        for candidate in self.filtered_news:
            write_count.write(candidate + ": " + str(len(self.filtered_news[candidate])) + "\n")
        write_count.close()


if __name__ == '__main__':
    company_analyst = CompanyAnalyst()
    company_analyst()
