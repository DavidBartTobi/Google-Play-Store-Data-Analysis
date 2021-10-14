from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
import pandas as pd
import numpy as np
import urllib.robotparser
import matplotlib.pyplot as plt
import grid


class Program:

    def __init__(self, root):
        self.root = root
        self.filename = ''
        self.df = pd.DataFrame

        self.choose_button = ttk.Button(self.root, text="Choose File", command=lambda: self.Choose_File(),
                                       width=21, cursor='hand2')

        self.top_installed_button = ttk.Button(self.root, text="Top Installed Categories", command=lambda: self.Top_Installed(),
                                        width=23, cursor='hand2')

        self.price_installation_button = ttk.Button(self.root, text="Price-Installation", command=lambda: self.Price_To_Install(),
                              width=23, cursor='hand2')

        self.size_installation_button = ttk.Button(self.root, text="Size-Installation", command=lambda: self.Size_To_Install(),
                              width=23, cursor='hand2')

        self.reviews_rating_button = ttk.Button(self.root, text="Reviews-Rating",
                                                   command=lambda: self.Reviews_To_Rating(),
                                                   width=23, cursor='hand2')

        self.categories_button = ttk.Button(self.root, text="Category stats",
                                                command=lambda: self.Category_Stats(),
                                                width=23, cursor='hand2')

        self.statistics_button = ttk.Button(self.root, text="More Statistics",
                                                command=lambda: self.General_Stats(),
                                                width=23, cursor='hand2')


        grid.Main_Grid(self.choose_button)


    def Choose_File(self):
        self.filename = fd.askopenfilename()

        grid.Hide_Main_Grid(self.choose_button)
        grid.Statistic_Grid(self.top_installed_button, self.price_installation_button, self.size_installation_button,
                            self.reviews_rating_button, self.categories_button, self.statistics_button)

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url("https://www.etsy.com/robots.txt")
        rp.read()
        rp.crawl_delay("*")

        test_crawl_url = "https://play.google.com/store/apps/details?id=com.wildnotion.poetscorner"

        can_crawl_listings = rp.can_fetch("*", test_crawl_url)
        if not can_crawl_listings:
            raise ValueError

        df = pd.read_csv(self.filename)

        df['Installs'] = df['Installs'].str.replace('+', '').str.replace(',', '')
        df = df[df.Installs != '0']
        df = df.drop_duplicates().reset_index(drop=True)
        df = df[pd.to_numeric(df['Installs'], errors='coerce').notnull()].reset_index(drop=True)
        df[['Installs']] = df[['Installs']].apply(pd.to_numeric)
        self.df = df


    def Top_Installed(self):
        installs_per_category = self.df.groupby('Category')['Installs'].sum()
        installs_per_category = installs_per_category.reindex(list(self.df.Category.unique()), axis=0)
        installs_per_category = installs_per_category.to_frame()
        installs_per_category.reset_index(level=0, inplace=True)

        top = installs_per_category['Installs'].nlargest(15)
        top_installed = installs_per_category[installs_per_category.Installs.isin(top)]

        plt.figure(figsize=(11,7.5))
        plt.bar(top_installed['Category'], top_installed['Installs'], color='#4169E1')
        plt.suptitle('Installations per category', fontsize=10)
        plt.xlabel('Category', fontsize=10)
        plt.xticks(fontsize=7, rotation=30)

        for i, num in enumerate(top_installed['Installs']):
            plt.text(
                i,
                num + 10000,
                num,
                ha='center',
                fontsize=8)

        plt.show()


    def Price_To_Install(self):

        installs_to_price = self.df[['Price', 'Installs']]

        try:
            installs_to_price['Price'] = installs_to_price['Price'].str.replace('$', '')
        except:
            pass

        try:
            installs_to_price[['Price']] = installs_to_price[['Price']].apply(pd.to_numeric)
        except:
            pass

        installs_to_price.sort_values(by='Price', inplace=True)

        plt.figure(figsize=(10,5))
        plt.suptitle('Installs-Price', fontsize=10)
        plt.xlabel('Price', fontsize=10)
        plt.ylabel('Installations', fontsize=10)
        plt.plot(installs_to_price.Price, installs_to_price.Installs, color='red')
        plt.show()


    def Size_To_Install(self):

        installs_to_size = self.df[['Size', 'Installs']]
        installs_to_size.dropna(subset=['Size'], inplace=True)
        installs_to_size = installs_to_size[~(installs_to_size['Size'] == 'Varies with device')]

        installs_to_size = installs_to_size[~installs_to_size.Size.str.contains(',+')]
        installs_to_size = installs_to_size[~installs_to_size.Size.str.contains(
            'a|b|c|d|e|f|g|h|i|j|l|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|L|N|O|P|Q|R|S|T|U|V|W|X|Y|Z')]

        installs_to_size.dropna(subset=['Size'], inplace=True)

        installs_to_size.Size = round((installs_to_size.Size.replace(r'[kKmM]+$', '', regex=True).astype(float) * installs_to_size.Size.str.extract(
            r'[\d\.]+([kKmM]+)', expand=False)
                         .fillna(1).replace(['k', 'K', 'm', 'M'], [10 ** (-3), 10 ** (-3), 1, 1]).astype(float)), 3)

        installs_to_size = installs_to_size.reset_index(drop=True)
        installs_to_size[['Size']] = installs_to_size[['Size']].apply(pd.to_numeric)
        installs_to_size.sort_values(by='Size', inplace=True)

        plt.figure(figsize=(10, 6))
        plt.suptitle('Install-Size')
        plt.xlabel('Size', fontsize=10)
        plt.ylabel('Installations', fontsize=10)
        plt.plot(installs_to_size.Size, installs_to_size.Installs, color='#008000')
        plt.show()


    def Reviews_To_Rating(self):
        try:
            reviews_to_rating = self.df[['Reviews', 'Rating']]
            column_name = 'Reviews'
        except:
            try:
                reviews_to_rating = self.df[['Rating Count', 'Rating']]
                column_name = 'Rating Count'
            except:
                messagebox.showerror("Error", f"One of the columns does not exist in the database")
                return


        reviews_to_rating = reviews_to_rating[reviews_to_rating['Rating'].between(0, 5)]
        reviews_to_rating[column_name] = pd.to_numeric(reviews_to_rating[column_name], errors='coerce')
        reviews_to_rating = reviews_to_rating[reviews_to_rating[column_name].notna()]
        reviews_to_rating = reviews_to_rating[reviews_to_rating['Rating'].notna()]
        reviews_to_rating.sort_values(by=column_name, inplace=True)

        plt.figure(figsize=(11, 6))
        plt.suptitle('Reviews-Rating', fontsize=12)
        plt.xlabel('Reviews', fontsize=10)
        plt.ylabel('Rating', fontsize=10)
        plt.plot(reviews_to_rating[column_name], reviews_to_rating['Rating'])
        plt.show()


    def Category_Stats(self):

        categories = self.df

        categories['Category'] = categories['Category'].str.replace('\d+', '', regex=True).str.replace('.', '',
                                                                                                       regex=True).replace(
            '', np.nan, regex=True)

        categories.dropna(subset=['Category'], inplace=True)

        categories = categories.Category.to_frame()

        categories = categories.Category.value_counts().reset_index()

        plt.figure(figsize=(8,6.3))  # pie was smaller when it was 8,6
        plt.pie(categories['Category'], autopct='%1.1f%%', pctdistance=1.12)
        plt.legend(labels=categories['index'], loc='right', fontsize='xx-small', bbox_to_anchor=(1.11, 0.5))
        # plt.title('My Tasks')
        plt.axis('equal')
        plt.tight_layout()
        ax = plt.gca()
        ax.set_xlim(0, 0.2)
        plt.show()


    def General_Stats(self):

        plot_objects = plt.subplots(nrows=2, ncols=2, figsize=(13, 6))

        fig, ((ax1, ax2), (ax3, ax4)) = plot_objects

        # AX 1

        sizes = self.df
        sizes.dropna(subset=['Size'], inplace=True)

        sizes = self.df[~(self.df['Size'] == 'Varies with device')]
        varies_with_device = self.df[self.df['Size'] == 'Varies with device']

        sizes = sizes[~sizes.Size.str.contains(',+')]
        sizes = sizes[~sizes.Size.str.contains(
            'a|b|c|d|e|f|g|h|i|j|l|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|L|N|O|P|Q|R|S|T|U|V|W|X|Y|Z')]

        sizes.dropna(subset=['Size'], inplace=True)

        sizes.Size = round((sizes.Size.replace(r'[kKmM]+$', '', regex=True).astype(float) * sizes.Size.str.extract(
            r'[\d\.]+([kKmM]+)', expand=False)
                         .fillna(1).replace(['k', 'K', 'm', 'M'], [10 ** (-3), 10 ** (-3), 1, 1]).astype(float)), 3)

        sizes = sizes.Size.reset_index(drop=True)

        try:
            sizes = sizes.apply(pd.to_numeric)
        except:
            pass

        bin_ranges = [0, 10, 40, 80, 100]
        sizes = pd.Series(pd.cut(sizes, bin_ranges)).value_counts()
        sizes = sizes.add(pd.Series([len(varies_with_device)], index=['Varies with device']), fill_value=0)

        sizes = sizes.to_frame().reset_index()

        ax1.pie(sizes[0], autopct='%1.1f%%')
        ax1.legend(sizes['index'], loc='right', fontsize='x-small', bbox_to_anchor=(1.1, 0.5))
        ax1.set_title('App Size Data (in MB)')
        ax1.axis('equal')
        ax1.set_position([0.1, 0.55, 0.3, 0.35])

        # AX 2

        types = self.df

        try:
            types['Type'] = types['Type'].str.replace('\d+', '', regex=True).str.replace('.', '', regex=True).replace(
                '', np.nan, regex=True)
            types.dropna(subset=['Type'], inplace=True)
            types = types.Type.value_counts().reset_index()

            ax2.pie(types['Type'], autopct='%1.1f%%')

        except:

            types['Free'] = types['Free'].replace(True, 'Free').replace(False, 'Paid')
            types.dropna(subset=['Free'], inplace=True)
            types = types.Free.value_counts().reset_index()
            ax2.pie(types['Free'], autopct='%1.1f%%')

        ax2.legend(labels=types['index'], loc='right', bbox_to_anchor=(1, 0.5))
        ax2.set_title('Ratio of Free To Paid Apps')
        ax2.axis('equal')
        ax2.set_position([0.55, 0.55, 0.3, 0.35])

        # AX 3

        content_ratings = self.df

        content_ratings['Content Rating'] = content_ratings['Content Rating'].str.replace(
            '\d+', '',regex=True).str.replace('.', '', regex=True).replace(
            '', np.nan, regex=True)

        content_ratings.dropna(subset=['Content Rating'], inplace=True)
        content_ratings = content_ratings['Content Rating'].value_counts().reset_index()

        ax3.pie(content_ratings['Content Rating'], autopct='%1.1f%%')
        ax3.legend(labels=content_ratings['index'], loc='right', fontsize='x-small', bbox_to_anchor=(1.05, 0.5))
        ax3.set_title('Content Rating Data')
        ax3.axis('equal')
        ax3.set_position([0.1,0.1,0.3,0.35])


        # AX 4

        ratings = self.df
        ratings = ratings[ratings['Rating'].between(0, 5)]
        ratings.dropna(subset=['Rating'], inplace=True)
        ratings = ratings['Rating'].to_frame()
        ratings.sort_values(by='Rating', inplace=True)

        ax4.hist(ratings, bins=20, color='brown')
        ax4.set_title('App Rating Data')

        plt.show()

