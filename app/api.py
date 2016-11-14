from flask import Blueprint
from flask_restful import Api, Resource
from app.storage.model import District, Pharmacy, DBSession
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


class DistrictList(Resource):

    def get(self):
        session = DBSession()
        browser = webdriver.PhantomJS()
        browser.get('https://nobetci.ieo.org.tr/#!İstanbul/')

        soup = BeautifulSoup(browser.page_source)

        for d in soup.find_all('option'):
            print(d.get_text())
            dist_name = District(name=d.get_text())
            session.add(dist_name)
            session.commit()

        return {'status': 'OK'}


class PharmacyList(Resource):

    def get(self):

        url = str('https://nobetci.ieo.org.tr/#!İstanbul/')
        session = DBSession()
        district = session.query(District).all()
        for i in district:
            display = Display(visible=0, size=(800, 600))
            display.start()
            browser = webdriver.Firefox()
            browser.get(url + i.name)
            soap = BeautifulSoup(browser.page_source)
            pharmacy_list = soap.find_all(attrs={"class": "eczane_cont"})

            for d in pharmacy_list:
                name = d.h2.text
                tel = d.span.text.replace('Tel: ', '')
                address = d.find(attrs={"class": "adres"}
                                 ).text.replace('Adres: ', '')
                print(name, tel, address)
                pharmacy_data = Pharmacy(
                    pharmacy_name=name, telephone=tel,
                    address=address, district_id=i.id)

                session.add(pharmacy_data)
            session.commit()

            browser.quit()
            display.stop()

        return {'status': 'OK'}



api.add_resource(DistrictList, '/api/district')
api.add_resource(PharmacyList, '/api/pharmacy')
