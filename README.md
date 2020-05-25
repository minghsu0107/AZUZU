# AZUZU
![](https://i.imgur.com/LCKEW4i.png)
## Demo
Please visit the demo site [here](http://linux7.csie.ntu.edu.tw:7070).
## Features
- fast loading speed
- dynamic shopping cart with local storage
- queryset caching on a per user basis
- designed with a responsive user inteface

## Prerequisites
- `nginx>=1.17.3`
- `PostgreSQL>=12.1`

See more details in `requirements.txt`.

## Set Up
1. Run `pip install -r requirements.txt`.
2. Change the db setting to to your postgres db in `settings.py`.
3. Change the configuration path in `deployfiles/setting.ini` and `deployfiles/ecomsite_nginx.conf` to your project path.
4. Create soft link to `deployfiles/ecomsite_nginx.conf` from `sites-available/` or `servers/` in your nginx directory. Also remember to include this folder in `nginx.conf`.
5. Create superuser by running `python manage.py createsuperuser`.

## Usage
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```
Start server:
```
./start.sh
```
Stop server:
```
./stop.sh
```
## Note
By optimizing images, we can reduce the image size and hence increase the loading speed of our site and decrease the bandwidth. Here is how you optimize all product images:
```s=
pip3 install pillow optimize-images
optimize-images ./product_imgs
```
