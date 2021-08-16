-- Keep a log of any SQL queries you execute as you solve the mystery.
-- i start with the known data, witch are street and date and see what i get
SELECT * FROM crime_scene_reports WHERE street = "Chamberlin Street" AND year = 2020 AND month = 7 AND day = 28;

-- i get this description of the fraud """"Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.""""
-- i know the hour of the theft, i know the witnessess, they mention the courhouse, lets see what we can get from the transcripts

SELECT * FROM interviews WHERE transcript LIKE "%courthouse%" AND year = 2020 AND month = 7 AND day = 28;

-- i get exactly 3 transcript from this query, let's see if i get something interesting
-- 161 | Ruth | 2020 | 7 | 28 | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- 162 | Eugene | 2020 | 7 | 28 | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- 163 | Raymond | 2020 | 7 | 28 | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


-- probably the hints here i will find the 3 answers i'm looking for, i think i should triangulate, and put some information toghere later
-- devo mischiare e triangolare le finromazioni!

-- the first witness suggests i have to do someting with activity in the courthouse tab, at this date, later i will see.
SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND (minute >= 15 AND minute < 26);
-- we find 8 cars exiting here...

-- second witness we get the name of a street, so we can look for activity in ATM on that street. lets see what we get
SELECT * FROM atm_transactions WHERE atm_location = "Fifer Street" AND year = 2020 AND month = 7 AND day = 28;
-- but there are 9-10 results, too many

-- third witness we have a call here, we don't know by who
SELECT * FROM phone_calls WHERE duration < 60 AND year = 2020 AND month = 7 AND day = 28;
-- about 10 possible answers here too, i have to put some information together now.

-- check if there are some people with atm and license plate we are looking

SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND (minute >= 15 AND minute < 26))
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location = "Fifer Street" AND year = 2020 AND month = 7 AND day = 28));

-- i get 4 possibile people, thats so nice!

-- now i check for the number too!
SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND (minute >= 15 AND minute < 26))
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location = "Fifer Street" AND year = 2020 AND month = 7 AND day = 28))
AND phone_number IN (SELECT caller FROM phone_calls WHERE duration < 60 AND year = 2020 AND month = 7 AND day = 28);

-- i get two possibile people
-- 514354 | Russell | (770) 555-1861 | 3592750733 | 322W7JE
-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X

-- lets see who they were calling
SELECT * FROM phone_calls WHERE duration < 60 AND year = 2020 AND month = 7 AND day = 28 AND caller IN (SELECT phone_number FROM people WHERE name = "Russell" OR name = "Ernest");
-- 233 | (367) 555-5533 | (375) 555-8161 | 2020 | 7 | 28 | 45
-- 255 | (770) 555-1861 | (725) 555-3243 | 2020 | 7 | 28 | 49
SELECT * FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE duration < 60 AND year = 2020 AND month = 7 AND day = 28 AND caller IN (SELECT phone_number FROM people WHERE name = "Russell" OR name = "Ernest"));
-- 847116 | Philip | (725) 555-3243 | 3391710505 | GW362R6
-- 864400 | Berthold | (375) 555-8161 |  | 4V16VO0

-- lets make the couples, by knowing the calls:
-- Russell - Philip
-- Ernest - Berthold
-- one of this two couple will be in a flight

-- lets see the flights the next day, as witnesse 3 told us
SELECT * FROM flights WHERE  year = 2020 AND month = 7 AND day = 29 ORDER BY hour, minute;
-- 36 | 8 | 4 | 2020 | 7 | 29 | 8 | 20
-- 43 | 8 | 1 | 2020 | 7 | 29 | 9 | 30
-- 23 | 8 | 11 | 2020 | 7 | 29 | 12 | 15
-- 53 | 8 | 9 | 2020 | 7 | 29 | 15 | 20
-- 18 | 8 | 6 | 2020 | 7 | 29 | 16 | 0
-- this is fine :D, we have to take the earliest flight

-- checking if one of the two was on the flight:
SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE  year = 2020 AND month = 7 AND day = 29 AND hour = 8 AND minute = 20)) AND (name = "Russell" OR name = "Ernest");

-- we see its Ernest, he called Berthold, he is going to airport number 4, lets check that airport and we have it all.

SELECT * FROM airports WHERE id = 4;
-- 4 | LHR | Heathrow Airport | London Flying to london? ahah, got ya