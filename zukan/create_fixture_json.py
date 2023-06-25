import json

def main():
    # 'model', 'pk', 'fields': 'name', 'slug', 'image', 'is_public'

    zukan_data = []
    i = 1
    while i < 40:
        zukan_data.append(
            {
            "model": "zukan.catzukan",
            "fields": {
                "name": f"My Cat {i}",
                "slug": f"my-cat-{i}",
                "image": "zukan/cat/cat_public_domain.webp",
                "is_public": True
                }
            }
        )
        zukan_data.append(
            {
            "model": "zukan.dogzukan",
            "fields": {
                "name": f"My Dog {i}",
                "slug": f"my-dog-{i}",
                "image": "zukan/dog/dog_public_domain.webp",
                "is_public": True
                }
            }
        )
        i += 1
    with open('zukan/fixture/zukan_initial_dump.json', 'w') as f:
        json.dump(zukan_data, f, indent=4)


if __name__ == '__main__':
    main()