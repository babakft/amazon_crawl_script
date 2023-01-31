import requests


class ImageDownloader:
    @staticmethod
    def get(link):
        try:
            response = requests.get(link, stream=True)
        except requests.exceptions.ConnectTimeout or requests.exceptions.ConnectionError:
            response = None
            print("Amazon refuses the request to download images. \n")
        return response

    def download_and_save_to_disk(self, path, product_json):
        image = product_json["image_url"]
        response = self.get(image)

        if response is not None:
            unique_attr = product_json['details']['product_information'].get(" ASIN ",
                                                                             product_json['title'].split(" ")[0])

            print(f"****downloading {product_json['title']} image... ")

            with open(f"{path}/{unique_attr}.jpg", 'ab') as file:
                file.write(response.content)
                for _ in response.iter_content():
                    file.write(response.content)
