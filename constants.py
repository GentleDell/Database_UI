# -*- coding: utf-8 -*-
"""
Created on Fri May 24 20:09:58 2019

@author: Gentle Deng
"""

TABEL_LIST = ['Amenities', 'Attributes',  'Avg_price',  'Calendar' ,
             'Capacity' , 'Hosts'     ,  'Listing'  ,  'Locations',
             'Obtain'   , 'Provide'   ,  'Requirements','Reviews' ,
             'Scores'   , 'Verifications', 'Verify'      ]

COLUNM_LIST = [['ame_id', 'amenities'],
               ['attr_id', 'property_type', 'room_type', 'accomodates', 
                'bathrooms', 'bedrooms', 'beds', 'bed_type', 'square_feet',
                'is_business_travel_ready'],
               ['avg_p_id', 'price', 'weekly_price', 'monthly_price', 
                'security_deposit', 'cleaning_fee'],
               ['list_id', 'date_', 'price'],
               ['cap_id', 'guests_included', 'extra_people',  
                'minimum_nights', 'maximum_nights'],
               ['host_id', 'host_url', 'host_name',  'host_since', 
                'host_response_time','host_response_rate','host_thumbnail_url',
                'host_picture_url', 'host_neighbourhood', 'host_about'],
               ['list_id', 'host_id', 'loc_id', 'cap_id', 'attr_id', 'req_id', 
                'avg_p_id', 'list_url', 'list_name',  'picture_url', 'latitude', 
                'longitude','dsummary','dspace', 'description', 'neighborhood_overview', 
                'notes', 'transit','daccess','interaction', 'house_rules'],
               ['loc_Id', 'country', 'country_code',  'city', 'city_name'],
               ['list_id', 'scor_id'],
               ['list_id', 'ame_id'],
               ['req_id', 'cancellation_policy', 'REQUIRE_GUEST_PROFILE_PICTURE', 'REQUIRE_GUEST_PHONE_VERIFICATION'],
               ['list_id', 'rev_id', 'date_',  'reviewer_id', 
                    'reviewer_name','comments'],
               ['scor_id', 'review_scores_rating', 'review_scores_accuracy',
                'review_scores_cleanliness'      , 'review_scores_checkin' , 
                'review_scores_communication'    , 'review_scores_location',
                'review_scores_value'],
               ['ver_id', 'verifications'],
               ['host_id', 'ver_id']]
               
TYPE_LIST = [# amenity
             ['int', 'str'],  
             # attribute
             ['int', 'str', 'str', 'int', 
              'int', 'int', 'int', 'str', 'float', 'str'],
             # avg_price
             ['int', 'str', 'str', 'str', 'str', 'str'],
             # calendar
             ['int', 'str', 'str'],
             # capacity
             ['int', 'int', 'str', 'int', 'int'],
             # host
              ['int', 'str', 'str',  'str', 'str','str','str','str', 'str', 'str'],
             # listing
             ['int', 'int', 'int', 'int', 'int', 'int', 'int', 'str', 'str',  'str', 'float', 
              'float','str','str', 'str', 'str', 'str', 'str','str','str', 'str'],
             # location
             ['int', 'str', 'str',  'str', 'str'],
             # obtain
             ['int', 'int'],
             # provide
             ['int', 'int'],
             # requirment
             ['int', 'str', 'str', 'str'],
             # review 
             ['int', 'int', 'str', 'int', 'str','str'],
             # score
             ['int', 'float', 'float', 'float', 'float' , 
              'float', 'float', 'float'],
             # verifications
             ['int', 'str'],
             # verify
             ['int', 'int']]
             
QUERY_LIST = [# Query 1
              [''' 
               SELECT LO.city_name, count(Attr.square_feet) AS Host_number  
                FROM Listing LI, Locations LO, Attributes Attr             
                WHERE LI.loc_id = LO.loc_id AND                            
                      LI.attr_id = Attr.attr_id AND                        
                      Attr.square_feet > = 0                               
                GROUP BY LO.city_name                                      
                ORDER BY COUNT(*) ASC
                '''],
               # Query 2
              ['''
               WITH T1 AS (SELECT H.host_neighbourhood, S.review_scores_rating, COUNT(1) OVER (PARTITION BY H.host_neighbourhood) AS Total_Rows,
               ROW_NUMBER() OVER (PARTITION BY H.host_neighbourhood ORDER BY S.review_scores_rating DESC) AS Row_DESC
                FROM Hosts H, Locations LO, Scores S, Listing LI, Obtain Obt
                WHERE LO.city_name = 'madrid' AND 
                      H.host_id = LI.host_id AND 
                      LI.loc_id = LO.loc_id AND 
                      Obt.list_id = LI.list_id AND 
                      Obt.scor_id = S.scor_id AND
                      S.review_scores_rating >= 0)
                SELECT T1.Host_neighbourhood, AVG(T1.review_scores_rating) AS median_score
                FROM T1
                WHERE (T1.ROW_DESC = T1.Total_Rows/2) OR (T1.ROW_DESC = T1.Total_Rows/2+1) OR (T1.Row_DESC = (1+T1.Total_Rows)/2)
                GROUP BY T1.Host_neighbourhood
                ORDER BY median_score DESC
                Fetch first 5 rows only
                '''],
              # Query 3
              ['''
               SELECT H.host_id, H.host_name, count(LI.list_id) as number_of_listings
                FROM Hosts H, Listing LI
                WHERE H.host_id = LI.host_id 
                GROUP BY H.host_id, H.host_name
                ORDER BY count(*) DESC
                Fetch first 1 rows only
                '''],
               # Query 4
              ['''
               SELECT H.host_id, H.host_name, AVG(cast(replace(replace(Cal.price,'$',''),',','')as float)) as AVG_price
                FROM Hosts H, Attributes Attr, AVG_prices AVGP, Listing LI, Locations LO, Calendar Cal,
                     Scores S, Requirements R, Verify Vy, Verifications V, Obtain Obt
                WHERE LI.host_id = H.host_id 
                      AND LI.loc_id = LO.loc_id 
                      AND Cal.list_id = LI.list_id
                      AND LI.attr_id = Attr.attr_id 
                      AND LI.req_id = R.req_id 
                      AND LI.avg_P_id = AVGP.avg_P_id 
                      AND LI.list_id = Obt.list_id 
                      AND Obt.scor_id =S.scor_id 
                      AND R.req_id = LI.req_id 
                      AND Vy.host_id = H.host_id 
                      AND Vy.ver_id = V.ver_id  
                      AND R.cancellation_policy = 'flexible' 
                      AND Attr.property_type = 'Apartment' 
                      AND LO.city_name = 'berlin' 
                      AND V.verifications = 'government_id'
                      AND Attr.beds >= 2 
                      AND S.review_scores_location >= 8     
                      AND TO_DATE(Cal.date_, 'YYYY-MM-DD') between TO_DATE('2019-03-01', 'YYYY-MM-DD')
                      AND TO_DATE('2019-04-30', 'YYYY-MM-DD')
                GROUP BY H.host_id, H.host_name
                ORDER BY AVG_price ASC
                Fetch first 5 rows only
               '''],
              # Query 5
              ['''
               WITH T1 AS (SELECT LI.list_id, LI.list_name, Ame.amenities
                            FROM Listing LI, Amenities Ame, Provide Pro
                            WHERE Pro.list_id = LI.list_id AND 
                                  Pro.ame_id = Ame.ame_id AND
                                 (Ame.amenities = 'Wifi' OR
                                  Ame.amenities = 'TV' OR
                                  Ame.amenities = 'Internet' OR
                                  Ame.amenities = 'Free street parking')),
                     T2 AS (SELECT T1.list_id, T1.list_name
                            FROM T1                        
                            WHERE T1.list_id IN (
                                  SELECT list_id
                                  FROM T1      
                                  GROUP BY list_id
                                  HAVING COUNT(*) > 1)),
                     T3 AS (SELECT T2.list_id, T2.list_name
                            FROM T2
                            GROUP BY T2.list_id, T2.list_name),
                     T4 AS (SELECT Attr.accomodates, T3.list_id, T3.list_name, S.review_scores_rating,
                                   ROW_NUMBER() OVER (PARTITION BY Attr.accomodates ORDER BY Attr.accomodates ASC, S.review_scores_rating DESC) AS ROWNUMBER
                            FROM Scores S, Attributes Attr, Obtain Obt, Listing LI, T3
                            WHERE Obt.list_id = LI.list_id AND 
                                  Obt.scor_id = S.scor_id AND 
                                  Attr.attr_id = LI.attr_id AND
                                  T3.list_id = LI.list_id AND
                                  S.review_scores_rating >= 0 
                            GROUP BY Attr.accomodates, T3.list_id, T3.list_name, S.review_scores_rating)
                 SELECT *
                 FROM T4
                 WHERE ROWNUMBER <= 5
               '''],
              # Query 6
              ['''
               WITH T1 AS (SELECT H.host_id, H.host_name, LI.list_id, LI.list_name, count(Rev.rev_id) AS number_of_reviews,
                                   ROW_NUMBER() OVER (PARTITION BY H.host_id ORDER BY H.host_id ASC) AS ROWNUMBER
                            FROM Hosts H, Listing LI, Reviews Rev
                            WHERE Rev.list_id = LI.list_id AND 
                                  H.host_id = LI.host_id 
                            GROUP BY H.host_id, H.host_name, LI.list_id, LI.list_name)
                SELECT *
                FROM T1
                WHERE ROWNUMBER <= 3
               '''],
              # Query 7
              ['''
               select h.host_neighbourhood, am.amenities, count(am.amenities)
                from  listing s, locations l, hosts h, amenities am, provide p, attributes ap
                where s.loc_id = l.loc_id and s.host_id = h.host_id and l.city_name = 'berlin' and s.attr_id = ap.attr_id and s.list_id = p.list_id and p.ame_id = am.ame_id
                group by h.host_neighbourhood, am.amenities
                order by h.host_neighbourhood, count(am.amenities) desc
               '''],
              # Query 8
              ['''
               select c1.t1 - c2.t2
                from (select avg(s.REVIEW_SCORES_COMMUNICATION) as t1
                from listing l, obtain o, scores s
                where l.list_id = o.list_id and o.scor_id = s.scor_id and   l.host_id = (select h.host_id
                                                                                      from hosts h, verify vf, verifications v
                                                                                      where h.host_id = vf.host_id and vf.ver_id = v.ver_id
                                                                                      group by h.HOST_ID
                                                                                      order by count(v.verifications) desc
                                                                                      fetch first 1 rows only))c1,
                (select avg(s.REVIEW_SCORES_COMMUNICATION) as t2
                from listing l, obtain o, scores s
                where l.list_id = o.list_id and o.scor_id = s.scor_id and   l.host_id = (select h.host_id
                                                                                      from hosts h, verify vf, verifications v
                                                                                      where h.host_id = vf.host_id and vf.ver_id = v.ver_id
                                                                                      group by h.HOST_ID
                                                                                      order by count(v.verifications) 
                                                                                      fetch first 1 rows only)) c2
               '''],
              # Query 9
              ['''
               select l.city_name
                from listing s,   locations l, reviews r , attributes attr
                where attr.ATTR_ID = s.ATTR_ID and s.loc_id = l.loc_id and s.list_id = r.list_id and attr.room_type in (select c1.room_type
                from (select a.room_type, avg(a.accomodates) as t1
                from attributes a
                group by a.room_type) c1
                where c1.t1 >=3)
                group by l.city_name
                order by count(r.rev_id) desc
                fetch first 1 rows only
               '''],
              # Query 10
              ['''
               select c1.h1
                from (select h.host_neighbourhood as h1, count(s.list_id) as h2
                from  locations l, listing s, hosts h
                where  l.loc_id = s.loc_id and s.host_id = h.host_id and l.city_name = 'madrid'
                group by h.host_neighbourhood) c1
                where (select count(list_id)
                from  locations l2, listing s2, hosts h2
                where l2.loc_id = s2.loc_id and s2.host_id = h2.host_id and l2.city_name = 'madrid' and h2.host_neighbourhood = c1.h1 and (select count(*) from calendar c where c.list_id = s2.list_id and substr(c.date_,1,4)='2019')>0 and cast(to_date(h2.host_since,'YYYY-MM-DD') as date) <=to_date('2017-06-01','YYYY-MM-DD')
                )>0.5 * c1.h2
               '''],
              # Query 11
              ['''
               select c1.l1
                from (select l.country as l1, count(s.list_id) as l2
                from listing s, locations l
                where s.loc_id = l.loc_id
                group by l.country) c1
                where (select count(s2.list_id) 
                from listing s2, locations l3
                where s2.loc_id = l3.loc_id and l3.country=c1.l1 and (select count(*) from calendar c where c.list_id = s2.list_id and substr(c.date_,1,4)='2018')>0)>=0.2*c1.l2
               '''],
              # Query 12
              ['''
               select c1.h1
                from (select h.host_neighbourhood as h1, count(list_id) as h2
                from  locations l, listing s, hosts h
                where  l.loc_id = s.loc_id and s.host_id = h.host_id and l.city_name = 'barcelona'
                group by h.host_neighbourhood) c1
                where (select count(list_id)
                from  locations l2, listing s2, hosts h2, requirements r2
                where l2.loc_id = s2.loc_id and s2.host_id = h2.host_id and l2.city_name = 'barcelona' and h2.host_neighbourhood = c1.h1 and s2.req_id = r2.req_id and r2.cancellation_policy = 'strict_14_with_grace_period'
                )>0.05 * c1.h2
               ''']]