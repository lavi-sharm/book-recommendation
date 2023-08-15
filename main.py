{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.6.5"
    },
    "colab": {
      "name": "fcc_book_recommendation_knn.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/a-mt/fcc-book-recommendation-knn/blob/main/fcc_book_recommendation_knn.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "uGd4NYQX1Rf_"
      },
      "source": [
        "## Instructions\n",
        "\n",
        "In this challenge, you will create a book recommendation algorithm using **K-Nearest Neighbors**.\n",
        "\n",
        "You will use the [Book-Crossings dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/). This dataset contains 1.1 million ratings (scale of 1-10) of 270,000 books by 90,000 users. \n",
        "\n",
        "After importing and cleaning the data, use `NearestNeighbors` from `sklearn.neighbors` to develop a model that shows books that are similar to a given book. The Nearest Neighbors algorithm measures distance to determine the “closeness” of instances.\n",
        "\n",
        "Create a function named `get_recommends` that takes a book title (from the dataset) as an argument and returns a list of 5 similar books with their distances from the book argument.\n",
        "\n",
        "This code:\n",
        "\n",
        "`get_recommends(\"The Queen of the Damned (Vampire Chronicles (Paperback))\")`\n",
        "\n",
        "should return:\n",
        "\n",
        "```\n",
        "[\n",
        "  'The Queen of the Damned (Vampire Chronicles (Paperback))',\n",
        "  [\n",
        "    ['Catch 22', 0.793983519077301], \n",
        "    ['The Witching Hour (Lives of the Mayfair Witches)', 0.7448656558990479], \n",
        "    ['Interview with the Vampire', 0.7345068454742432],\n",
        "    ['The Tale of the Body Thief (Vampire Chronicles (Paperback))', 0.5376338362693787],\n",
        "    ['The Vampire Lestat (Vampire Chronicles, Book II)', 0.5178412199020386]\n",
        "  ]\n",
        "]\n",
        "```\n",
        "\n",
        "Notice that the data returned from `get_recommends()` is a list. The first element in the list is the book title passed in to the function. The second element in the list is a list of five more lists. Each of the five lists contains a recommended book and the distance from the recommended book to the book passed in to the function.\n",
        "\n",
        "If you graph the dataset (optional), you will notice that most books are not rated frequently. To ensure statistical significance, remove from the dataset users with less than 200 ratings and books with less than 100 ratings.\n",
        "\n",
        "The first three cells import libraries you may need and the data to use. The final cell is for testing. Write all your code in between those cells.\n",
        "\n",
        "## Load libraries"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Y1onB6kUvo4Z"
      },
      "source": [
        "# import libraries (you may add additional imports but you may not have to)\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "from scipy.sparse import csr_matrix\n",
        "from sklearn.neighbors import NearestNeighbors\n",
        "import matplotlib.pyplot as plt"
      ],
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "q_F2GF4KdnDA"
      },
      "source": [
        "## Import data"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "iAQGqqO_vo4d",
        "outputId": "fed52dcb-5c43-48fa-cc01-9a74a8c51998",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 278
        }
      },
      "source": [
        "# get data files\n",
        "!wget https://cdn.freecodecamp.org/project-data/books/book-crossings.zip\n",
        "\n",
        "!unzip book-crossings.zip"
      ],
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "--2020-10-15 08:42:49--  https://cdn.freecodecamp.org/project-data/books/book-crossings.zip\n",
            "Resolving cdn.freecodecamp.org (cdn.freecodecamp.org)... 104.26.3.33, 172.67.70.149, 104.26.2.33, ...\n",
            "Connecting to cdn.freecodecamp.org (cdn.freecodecamp.org)|104.26.3.33|:443... connected.\n",
            "HTTP request sent, awaiting response... 200 OK\n",
            "Length: unspecified [application/zip]\n",
            "Saving to: ‘book-crossings.zip’\n",
            "\n",
            "book-crossings.zip      [               <=>  ]  24.88M  2.24MB/s    in 11s     \n",
            "\n",
            "2020-10-15 08:43:01 (2.25 MB/s) - ‘book-crossings.zip’ saved [26085508]\n",
            "\n",
            "Archive:  book-crossings.zip\n",
            "  inflating: BX-Book-Ratings.csv     \n",
            "  inflating: BX-Books.csv            \n",
            "  inflating: BX-Users.csv            \n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "mnK28gS_zv7-"
      },
      "source": [
        "books_filename   = 'BX-Books.csv'\n",
        "ratings_filename = 'BX-Book-Ratings.csv'"
      ],
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "NClILWOiEd6Q",
        "outputId": "646c5ac7-784f-436b-f394-a8f1a5c5d8ef",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 206
        }
      },
      "source": [
        "# import csv data into dataframes\n",
        "df_books = pd.read_csv(\n",
        "    books_filename,\n",
        "    encoding = \"ISO-8859-1\",\n",
        "    sep=\";\",\n",
        "    header=0,\n",
        "    names=['isbn', 'title', 'author'],\n",
        "    usecols=['isbn', 'title', 'author'],\n",
        "    dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})\n",
        "\n",
        "df_ratings = pd.read_csv(\n",
        "    ratings_filename,\n",
        "    encoding = \"ISO-8859-1\",\n",
        "    sep=\";\",\n",
        "    header=0,\n",
        "    names=['user', 'isbn', 'rating'],\n",
        "    usecols=['user', 'isbn', 'rating'],\n",
        "    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})\n",
        "\n",
        "df_books.head()"
      ],
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>isbn</th>\n",
              "      <th>title</th>\n",
              "      <th>author</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>0195153448</td>\n",
              "      <td>Classical Mythology</td>\n",
              "      <td>Mark P. O. Morford</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>0002005018</td>\n",
              "      <td>Clara Callan</td>\n",
              "      <td>Richard Bruce Wright</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>0060973129</td>\n",
              "      <td>Decision in Normandy</td>\n",
              "      <td>Carlo D'Este</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>0374157065</td>\n",
              "      <td>Flu: The Story of the Great Influenza Pandemic...</td>\n",
              "      <td>Gina Bari Kolata</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>0393045218</td>\n",
              "      <td>The Mummies of Urumchi</td>\n",
              "      <td>E. J. W. Barber</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "         isbn  ...                author\n",
              "0  0195153448  ...    Mark P. O. Morford\n",
              "1  0002005018  ...  Richard Bruce Wright\n",
              "2  0060973129  ...          Carlo D'Este\n",
              "3  0374157065  ...      Gina Bari Kolata\n",
              "4  0393045218  ...       E. J. W. Barber\n",
              "\n",
              "[5 rows x 3 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 4
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "xAcXjkCFCh0A",
        "outputId": "d1b83c61-6c68-463c-8431-48a6c8111051",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 206
        }
      },
      "source": [
        "df_ratings.head()"
      ],
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>user</th>\n",
              "      <th>isbn</th>\n",
              "      <th>rating</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>276725</td>\n",
              "      <td>034545104X</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>276726</td>\n",
              "      <td>0155061224</td>\n",
              "      <td>5.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>276727</td>\n",
              "      <td>0446520802</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>276729</td>\n",
              "      <td>052165615X</td>\n",
              "      <td>3.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>276729</td>\n",
              "      <td>0521795028</td>\n",
              "      <td>6.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "     user        isbn  rating\n",
              "0  276725  034545104X     0.0\n",
              "1  276726  0155061224     5.0\n",
              "2  276727  0446520802     0.0\n",
              "3  276729  052165615X     3.0\n",
              "4  276729  0521795028     6.0"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 5
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "v6uzonKzeF6E"
      },
      "source": [
        "## Check null data"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "-JXLIVdreH-C",
        "outputId": "0f0da637-c58d-4f45-cbb3-f1ad786e6ad9",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 86
        }
      },
      "source": [
        "df_books.isnull().sum()"
      ],
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "isbn      0\n",
              "title     0\n",
              "author    1\n",
              "dtype: int64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 6
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "hwMNQWZneW3_",
        "outputId": "a2cd7914-4238-41d3-8e78-4fb4fa14041f",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 86
        }
      },
      "source": [
        "df_ratings.isnull().sum()"
      ],
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "user      0\n",
              "isbn      0\n",
              "rating    0\n",
              "dtype: int64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 7
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "N5mpprP6eag1"
      },
      "source": [
        "df_books.dropna(inplace=True)"
      ],
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "jYLLOpaBefJh",
        "outputId": "3e2e6388-287d-4fb3-fc62-090721b27522",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 86
        }
      },
      "source": [
        "df_books.isnull().sum()"
      ],
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "isbn      0\n",
              "title     0\n",
              "author    0\n",
              "dtype: int64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 9
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "IUL71rYPfKX7"
      },
      "source": [
        "## Remove users with less than 200 ratings"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "TE8DC7VJi_zO",
        "outputId": "0596c486-9a80-4d93-8238-4c4cf94e0c94",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "df_ratings.shape"
      ],
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(1149780, 3)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 10
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "2h9vkU0xhIvQ",
        "outputId": "92c9bdb3-4beb-4a64-e19e-f986973a544b",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 121
        }
      },
      "source": [
        "ratings = df_ratings['user'].value_counts()\n",
        "ratings.sort_values(ascending=False).head()"
      ],
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "11676     13602\n",
              "198711     7550\n",
              "153662     6109\n",
              "98391      5891\n",
              "35859      5850\n",
              "Name: user, dtype: int64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 11
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "07yE5rUyjM_T",
        "outputId": "e716315a-375c-4b79-8923-89bee494f680",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "len(ratings[ratings < 200])"
      ],
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "104378"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 12
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "m5qCNGD3mx9R",
        "outputId": "8f1c5fec-86db-47ef-e30a-01c72d7cf9bb",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "df_ratings['user'].isin(ratings[ratings < 200].index).sum()"
      ],
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "622224"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 13
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "cknVbnKri6_c",
        "outputId": "f442b6a1-46ce-4675-fd2e-4984b9137b12",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "df_ratings_rm = df_ratings[\n",
        "  ~df_ratings['user'].isin(ratings[ratings < 200].index)\n",
        "]\n",
        "df_ratings_rm.shape"
      ],
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(527556, 3)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 14
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "JcAof3kQn2NV"
      },
      "source": [
        "## Remove books with less than 100 ratings"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "3ucTVN7CevEN",
        "outputId": "e67d1138-1fe0-4cfa-9df1-0be277b25da5",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 121
        }
      },
      "source": [
        "ratings = df_ratings['isbn'].value_counts() # we have to use the original df_ratings to pass the challenge\n",
        "ratings.sort_values(ascending=False).head()"
      ],
      "execution_count": 15,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "0971880107    2502\n",
              "0316666343    1295\n",
              "0385504209     883\n",
              "0060928336     732\n",
              "0312195516     723\n",
              "Name: isbn, dtype: int64"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 15
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "85aIP2kph2q0",
        "outputId": "c83195f0-e16e-4291-f1cd-4cf7463182d1",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "len(ratings[ratings < 100])"
      ],
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "339825"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 16
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "oW68SnJQqU4E",
        "outputId": "f105035e-e6eb-411b-fcac-1004fe4a67fa",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "df_books['isbn'].isin(ratings[ratings < 100].index).sum()"
      ],
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "269442"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 17
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "8WMIqkWNfVDd",
        "outputId": "e2a67008-2d74-4b41-c62c-68fb15ef89d6",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "df_ratings_rm = df_ratings_rm[\n",
        "  ~df_ratings_rm['isbn'].isin(ratings[ratings < 100].index)\n",
        "]\n",
        "df_ratings_rm.shape"
      ],
      "execution_count": 18,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(49781, 3)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 18
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "16CsPkMrpnQ1",
        "outputId": "8a311083-ec37-4952-b3bb-12fd54147b5a",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 104
        }
      },
      "source": [
        "# These should exist\n",
        "books = [\"Where the Heart Is (Oprah's Book Club (Paperback))\",\n",
        "        \"I'll Be Seeing You\",\n",
        "        \"The Weight of Water\",\n",
        "        \"The Surgeon\",\n",
        "        \"I Know This Much Is True\"]\n",
        "\n",
        "for book in books:\n",
        "  print(df_ratings_rm.isbn.isin(df_books[df_books.title == book].isbn).sum())"
      ],
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "183\n",
            "75\n",
            "49\n",
            "57\n",
            "77\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "Bd8nZD08QIvR"
      },
      "source": [
        "## Prepare dataset for KNN"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "39VgsA7MNiiA",
        "outputId": "bf221282-0017-46de-85bc-c621204f35e7",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 287
        }
      },
      "source": [
        "df = df_ratings_rm.pivot_table(index=['user'],columns=['isbn'],values='rating').fillna(0).T\n",
        "df.head()"
      ],
      "execution_count": 20,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th>user</th>\n",
              "      <th>254</th>\n",
              "      <th>2276</th>\n",
              "      <th>2766</th>\n",
              "      <th>2977</th>\n",
              "      <th>3363</th>\n",
              "      <th>4017</th>\n",
              "      <th>4385</th>\n",
              "      <th>6242</th>\n",
              "      <th>6251</th>\n",
              "      <th>6323</th>\n",
              "      <th>6543</th>\n",
              "      <th>6563</th>\n",
              "      <th>6575</th>\n",
              "      <th>7158</th>\n",
              "      <th>7286</th>\n",
              "      <th>7346</th>\n",
              "      <th>7915</th>\n",
              "      <th>8067</th>\n",
              "      <th>8245</th>\n",
              "      <th>8681</th>\n",
              "      <th>8936</th>\n",
              "      <th>9856</th>\n",
              "      <th>10447</th>\n",
              "      <th>10819</th>\n",
              "      <th>11601</th>\n",
              "      <th>11676</th>\n",
              "      <th>11993</th>\n",
              "      <th>12538</th>\n",
              "      <th>12824</th>\n",
              "      <th>12982</th>\n",
              "      <th>13082</th>\n",
              "      <th>13273</th>\n",
              "      <th>13552</th>\n",
              "      <th>13850</th>\n",
              "      <th>14422</th>\n",
              "      <th>14521</th>\n",
              "      <th>15408</th>\n",
              "      <th>15418</th>\n",
              "      <th>15957</th>\n",
              "      <th>16106</th>\n",
              "      <th>...</th>\n",
              "      <th>264317</th>\n",
              "      <th>264321</th>\n",
              "      <th>264637</th>\n",
              "      <th>265115</th>\n",
              "      <th>265313</th>\n",
              "      <th>265595</th>\n",
              "      <th>265889</th>\n",
              "      <th>266056</th>\n",
              "      <th>266226</th>\n",
              "      <th>266753</th>\n",
              "      <th>266865</th>\n",
              "      <th>266866</th>\n",
              "      <th>267635</th>\n",
              "      <th>268030</th>\n",
              "      <th>268032</th>\n",
              "      <th>268110</th>\n",
              "      <th>268330</th>\n",
              "      <th>268622</th>\n",
              "      <th>268932</th>\n",
              "      <th>269566</th>\n",
              "      <th>269719</th>\n",
              "      <th>269728</th>\n",
              "      <th>269890</th>\n",
              "      <th>270713</th>\n",
              "      <th>270820</th>\n",
              "      <th>271195</th>\n",
              "      <th>271284</th>\n",
              "      <th>271448</th>\n",
              "      <th>271705</th>\n",
              "      <th>273979</th>\n",
              "      <th>274004</th>\n",
              "      <th>274061</th>\n",
              "      <th>274301</th>\n",
              "      <th>274308</th>\n",
              "      <th>274808</th>\n",
              "      <th>275970</th>\n",
              "      <th>277427</th>\n",
              "      <th>277478</th>\n",
              "      <th>277639</th>\n",
              "      <th>278418</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>isbn</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>002542730X</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>6.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>10.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>7.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>10.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0060008032</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>8.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>6.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>8.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>8.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0060096195</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>8.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>10.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>7.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>006016848X</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>9.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>7.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0060173289</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 888 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "user        254     2276    2766    2977    ...  277427  277478  277639  278418\n",
              "isbn                                        ...                                \n",
              "002542730X     0.0     0.0     0.0     0.0  ...    10.0     0.0     0.0     0.0\n",
              "0060008032     0.0     0.0     0.0     0.0  ...     0.0     0.0     0.0     0.0\n",
              "0060096195     0.0     0.0     0.0     0.0  ...     0.0     0.0     0.0     0.0\n",
              "006016848X     0.0     0.0     0.0     0.0  ...     0.0     0.0     0.0     0.0\n",
              "0060173289     0.0     0.0     0.0     0.0  ...     0.0     0.0     0.0     0.0\n",
              "\n",
              "[5 rows x 888 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 20
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Wc2nLYqu6Brr"
      },
      "source": [
        "df.index = df.join(df_books.set_index('isbn'))['title']"
      ],
      "execution_count": 21,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "m9p7Jxh27EqR",
        "outputId": "b8e78d35-f23b-4927-e58b-261e3442271b",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 391
        }
      },
      "source": [
        "df = df.sort_index()\n",
        "df.head()"
      ],
      "execution_count": 22,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th>user</th>\n",
              "      <th>254</th>\n",
              "      <th>2276</th>\n",
              "      <th>2766</th>\n",
              "      <th>2977</th>\n",
              "      <th>3363</th>\n",
              "      <th>4017</th>\n",
              "      <th>4385</th>\n",
              "      <th>6242</th>\n",
              "      <th>6251</th>\n",
              "      <th>6323</th>\n",
              "      <th>6543</th>\n",
              "      <th>6563</th>\n",
              "      <th>6575</th>\n",
              "      <th>7158</th>\n",
              "      <th>7286</th>\n",
              "      <th>7346</th>\n",
              "      <th>7915</th>\n",
              "      <th>8067</th>\n",
              "      <th>8245</th>\n",
              "      <th>8681</th>\n",
              "      <th>8936</th>\n",
              "      <th>9856</th>\n",
              "      <th>10447</th>\n",
              "      <th>10819</th>\n",
              "      <th>11601</th>\n",
              "      <th>11676</th>\n",
              "      <th>11993</th>\n",
              "      <th>12538</th>\n",
              "      <th>12824</th>\n",
              "      <th>12982</th>\n",
              "      <th>13082</th>\n",
              "      <th>13273</th>\n",
              "      <th>13552</th>\n",
              "      <th>13850</th>\n",
              "      <th>14422</th>\n",
              "      <th>14521</th>\n",
              "      <th>15408</th>\n",
              "      <th>15418</th>\n",
              "      <th>15957</th>\n",
              "      <th>16106</th>\n",
              "      <th>...</th>\n",
              "      <th>264317</th>\n",
              "      <th>264321</th>\n",
              "      <th>264637</th>\n",
              "      <th>265115</th>\n",
              "      <th>265313</th>\n",
              "      <th>265595</th>\n",
              "      <th>265889</th>\n",
              "      <th>266056</th>\n",
              "      <th>266226</th>\n",
              "      <th>266753</th>\n",
              "      <th>266865</th>\n",
              "      <th>266866</th>\n",
              "      <th>267635</th>\n",
              "      <th>268030</th>\n",
              "      <th>268032</th>\n",
              "      <th>268110</th>\n",
              "      <th>268330</th>\n",
              "      <th>268622</th>\n",
              "      <th>268932</th>\n",
              "      <th>269566</th>\n",
              "      <th>269719</th>\n",
              "      <th>269728</th>\n",
              "      <th>269890</th>\n",
              "      <th>270713</th>\n",
              "      <th>270820</th>\n",
              "      <th>271195</th>\n",
              "      <th>271284</th>\n",
              "      <th>271448</th>\n",
              "      <th>271705</th>\n",
              "      <th>273979</th>\n",
              "      <th>274004</th>\n",
              "      <th>274061</th>\n",
              "      <th>274301</th>\n",
              "      <th>274308</th>\n",
              "      <th>274808</th>\n",
              "      <th>275970</th>\n",
              "      <th>277427</th>\n",
              "      <th>277478</th>\n",
              "      <th>277639</th>\n",
              "      <th>278418</th>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>title</th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "      <th></th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>1984</th>\n",
              "      <td>9.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>9.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>10.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1st to Die: A Novel</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>8.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1st to Die: A Novel</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>9.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>10.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>7.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2nd Chance</th>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>7.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2nd Chance</th>\n",
              "      <td>0.0</td>\n",
              "      <td>10.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>8.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 888 columns</p>\n",
              "</div>"
            ],
            "text/plain": [
              "user                 254     2276    2766    ...  277478  277639  278418\n",
              "title                                        ...                        \n",
              "1984                    9.0     0.0     0.0  ...     0.0     0.0     0.0\n",
              "1st to Die: A Novel     0.0     0.0     0.0  ...     0.0     0.0     0.0\n",
              "1st to Die: A Novel     0.0     0.0     0.0  ...     0.0     0.0     0.0\n",
              "2nd Chance              0.0     0.0     0.0  ...     0.0     0.0     0.0\n",
              "2nd Chance              0.0    10.0     0.0  ...     0.0     0.0     0.0\n",
              "\n",
              "[5 rows x 888 columns]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 22
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "eLksz27CwjWJ",
        "outputId": "bdaf02e9-dd49-47c6-9109-67bda779b62c",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 139
        }
      },
      "source": [
        "df.loc[\"The Queen of the Damned (Vampire Chronicles (Paperback))\"][:5]"
      ],
      "execution_count": 24,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "user\n",
              "254     0.0\n",
              "2276    0.0\n",
              "2766    0.0\n",
              "2977    0.0\n",
              "3363    0.0\n",
              "Name: The Queen of the Damned (Vampire Chronicles (Paperback)), dtype: float32"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 24
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "aFO7pV07eKAi"
      },
      "source": [
        "## Build model"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "CTcoap9ztEi_",
        "outputId": "fd395131-ce90-45db-e8d2-a6089734b3ca",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 69
        }
      },
      "source": [
        "model = NearestNeighbors(metric='cosine')\n",
        "model.fit(df.values)"
      ],
      "execution_count": 25,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "NearestNeighbors(algorithm='auto', leaf_size=30, metric='cosine',\n",
              "                 metric_params=None, n_jobs=None, n_neighbors=5, p=2,\n",
              "                 radius=1.0)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 25
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XYRCY6yfJWr9"
      },
      "source": [
        "## Create get_recommends()"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "6wSgRrlcxwWL",
        "outputId": "43687249-66f0-4402-a6cf-eca43b59b7c6",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "df.iloc[0].shape"
      ],
      "execution_count": 26,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(888,)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 26
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "p1h7sSndx2pN",
        "outputId": "695157b5-3b5b-49c5-8258-3da2555876d7",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        }
      },
      "source": [
        "title = 'The Queen of the Damned (Vampire Chronicles (Paperback))'\n",
        "df.loc[title].shape"
      ],
      "execution_count": 27,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(888,)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 27
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "IUQR7yYHu3iX",
        "outputId": "6d9c8a12-9de8-400c-9407-48bef9e540c3",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 52
        }
      },
      "source": [
        "distance, indice = model.kneighbors([df.loc[title].values], n_neighbors=6)\n",
        "\n",
        "print(distance)\n",
        "print(indice)"
      ],
      "execution_count": 28,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[[0.         0.51784116 0.53763384 0.73450685 0.74486566 0.7939835 ]]\n",
            "[[612 660 648 272 667 110]]\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "CB4AEptUys8S",
        "outputId": "86aca93c-4b65-4d6e-c072-5688fc0a5ab7",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 121
        }
      },
      "source": [
        "df.iloc[indice[0]].index.values"
      ],
      "execution_count": 29,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "array(['The Queen of the Damned (Vampire Chronicles (Paperback))',\n",
              "       'The Vampire Lestat (Vampire Chronicles, Book II)',\n",
              "       'The Tale of the Body Thief (Vampire Chronicles (Paperback))',\n",
              "       'Interview with the Vampire',\n",
              "       'The Witching Hour (Lives of the Mayfair Witches)', 'Catch 22'],\n",
              "      dtype=object)"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 29
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "qIfyeVCtJR7n",
        "outputId": "2fd68da3-a475-4ff2-9e5f-529a817ddba5",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 238
        }
      },
      "source": [
        "pd.DataFrame({\n",
        "    'title'   : df.iloc[indice[0]].index.values,\n",
        "    'distance': distance[0]\n",
        "}) \\\n",
        ".sort_values(by='distance', ascending=False)"
      ],
      "execution_count": 30,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>title</th>\n",
              "      <th>distance</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>Catch 22</td>\n",
              "      <td>0.793984</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>The Witching Hour (Lives of the Mayfair Witches)</td>\n",
              "      <td>0.744866</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>Interview with the Vampire</td>\n",
              "      <td>0.734507</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>The Tale of the Body Thief (Vampire Chronicles...</td>\n",
              "      <td>0.537634</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>The Vampire Lestat (Vampire Chronicles, Book II)</td>\n",
              "      <td>0.517841</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>The Queen of the Damned (Vampire Chronicles (P...</td>\n",
              "      <td>0.000000</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>"
            ],
            "text/plain": [
              "                                               title  distance\n",
              "5                                           Catch 22  0.793984\n",
              "4   The Witching Hour (Lives of the Mayfair Witches)  0.744866\n",
              "3                         Interview with the Vampire  0.734507\n",
              "2  The Tale of the Body Thief (Vampire Chronicles...  0.537634\n",
              "1   The Vampire Lestat (Vampire Chronicles, Book II)  0.517841\n",
              "0  The Queen of the Damned (Vampire Chronicles (P...  0.000000"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 30
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "f5ZUd-L1SQz7"
      },
      "source": [
        "# function to return recommended books - this will be tested\n",
        "def get_recommends(title = \"\"):\n",
        "  try:\n",
        "    book = df.loc[title]\n",
        "  except KeyError as e:\n",
        "    print('The given book', e, 'does not exist')\n",
        "    return\n",
        "\n",
        "  distance, indice = model.kneighbors([book.values], n_neighbors=6)\n",
        "\n",
        "  recommended_books = pd.DataFrame({\n",
        "      'title'   : df.iloc[indice[0]].index.values,\n",
        "      'distance': distance[0]\n",
        "    }) \\\n",
        "    .sort_values(by='distance', ascending=False) \\\n",
        "    .head(5).values\n",
        "\n",
        "  return [title, recommended_books]"
      ],
      "execution_count": 31,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "sMVRQu-RMk5X",
        "outputId": "40ecbf4a-82fd-413d-b394-f8865a471870",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 173
        }
      },
      "source": [
        "get_recommends(\"The Queen of the Damned (Vampire Chronicles (Paperback))\")"
      ],
      "execution_count": 32,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['The Queen of the Damned (Vampire Chronicles (Paperback))',\n",
              " array([['Catch 22', 0.793983519077301],\n",
              "        ['The Witching Hour (Lives of the Mayfair Witches)',\n",
              "         0.7448656558990479],\n",
              "        ['Interview with the Vampire', 0.7345068454742432],\n",
              "        ['The Tale of the Body Thief (Vampire Chronicles (Paperback))',\n",
              "         0.5376338362693787],\n",
              "        ['The Vampire Lestat (Vampire Chronicles, Book II)',\n",
              "         0.5178411602973938]], dtype=object)]"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 32
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "eat9A2TKawHU"
      },
      "source": [
        "## Predict\n",
        "\n",
        "Use the cell below to test your function. The `test_book_recommendation()` function will inform you if you passed the challenge or need to keep trying."
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "jd2SLCh8oxMh",
        "outputId": "fd6819e3-e49b-4ef6-b28d-75188ec33b0a",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 121
        }
      },
      "source": [
        "books = get_recommends(\"Where the Heart Is (Oprah's Book Club (Paperback))\")\n",
        "print(books)\n",
        "\n",
        "def test_book_recommendation():\n",
        "  test_pass = True\n",
        "  recommends = get_recommends(\"Where the Heart Is (Oprah's Book Club (Paperback))\")\n",
        "  if recommends[0] != \"Where the Heart Is (Oprah's Book Club (Paperback))\":\n",
        "    test_pass = False\n",
        "  recommended_books = [\"I'll Be Seeing You\", 'The Weight of Water', 'The Surgeon', 'I Know This Much Is True']\n",
        "  recommended_books_dist = [0.8, 0.77, 0.77, 0.77]\n",
        "  for i in range(2): \n",
        "    if recommends[1][i][0] not in recommended_books:\n",
        "      test_pass = False\n",
        "    if abs(recommends[1][i][1] - recommended_books_dist[i]) >= 0.05:\n",
        "      test_pass = False\n",
        "  if test_pass:\n",
        "    print(\"You passed the challenge! 🎉🎉🎉🎉🎉\")\n",
        "  else:\n",
        "    print(\"You havn't passed yet. Keep trying!\")\n",
        "\n",
        "test_book_recommendation()"
      ],
      "execution_count": 33,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "[\"Where the Heart Is (Oprah's Book Club (Paperback))\", array([[\"I'll Be Seeing You\", 0.8016210794448853],\n",
            "       ['The Weight of Water', 0.7708583474159241],\n",
            "       ['The Surgeon', 0.7699410915374756],\n",
            "       ['I Know This Much Is True', 0.7677075266838074],\n",
            "       ['The Lovely Bones: A Novel', 0.7234864234924316]], dtype=object)]\n",
            "You passed the challenge! 🎉🎉🎉🎉🎉\n"
          ],
          "name": "stdout"
        }
      ]
    }
  ]
}
