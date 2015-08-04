#!/usr/bin/env python

import sys
from agol_util import AGOL_util

def test(secret):
    #init agol util and get auth token
    agol = AGOL_util('https://worldresources.maps.arcgis.com/sharing/rest',
                     'wri_ckan',
                     secret
                     )
    print agol.get_token()

    #copy shapefile from external url to agol
    res = agol.add_shapefile_from_url('http://data.wri.org/Aqueduct/aqueduct_global_dl_shp2.zip')
    itemId = res['id']
    print res

    #confirm copy completion
    agol.wait_for_completion(itemId)

    #publish shapefile as feature service
    res = agol.publish_shapefile(itemId)
    serviceId = res['services'][0]['serviceItemId']
    print res

    #add metadata to feature service
    metadata = {
        'title':'api uploaded feature layer',
        'thumbnailurl':'http://data.wri.org/Aqueduct/BWS_gme.png',
        'snippet':'A short description',
        'description':'This is the description of this data layer',
        'licenseInfo':'Creative Commons Attribution 4.0 International',
        'accessInformation':'WRI',
        'tags':'api, uploaded, feature layer'
        }
    print agol.update_item(serviceId, options=metadata)

    ODGroupID = '1c51076fb7e64302ba65afd011b08b79'
    #share feature service publicly and add to Open Data group
    print agol.share_items(serviceId, everyone='true', groups=ODGroupID)

    #itemId and serviceId should be saved for later management
    return itemId, serviceId

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python test.py <SECRET>"
    else:
        test(sys.argv[1])
