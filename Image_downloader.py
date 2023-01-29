import requests


class ImageDownloader:
    @staticmethod
    def get(link):
        try:
            response = requests.get(link, stream=True)
        except requests.exceptions.ConnectTimeout:
            response = None
            print("Amazon refuses the request to download images. \n")
        return response

    def download_and_save_to_disk(self, path, product_dictionary):
        image = product_dictionary["image_url"]
        response = self.get(image)

        if response is not None:
            unique_attr = product_dictionary['details']['product_information'].get(" ASIN ", product_dictionary['title'])

            print(f"downloading {product_dictionary['title']} image... ")

            with open(f"{path}/{unique_attr}.jpg", 'ab') as file:
                file.write(response.content)
                for _ in response.iter_content():
                    file.write(response.content)
