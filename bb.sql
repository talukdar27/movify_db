
SET GLOBAL event_scheduler = ON;

CREATE TABLE Bank_Details (
    Bank_Account_No VARCHAR(20) PRIMARY KEY,
    Bank_Name VARCHAR(50) NOT NULL,
    Bank_Branch_Code VARCHAR(10) NOT NULL
);

CREATE TABLE Account (
    Account_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Date_of_Birth DATE,
    Account_Type ENUM('General', 'Kids') NOT NULL,
    Date_of_First_Access DATE,
    Country VARCHAR(50),
    No_of_Active_Devices INT DEFAULT 1,
    Bank_Account_No VARCHAR(20),
    Last_Access_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Bank_Account_No) REFERENCES Bank_Details(Bank_Account_No) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Content (
    Content_ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(150) NOT NULL,
    Description TEXT,
    Country_of_Origin VARCHAR(50),
    Trailer BLOB,
    Avg_Rating FLOAT
);

CREATE TABLE Movies (
    Movie_ID INT PRIMARY KEY,
    Release_Year YEAR,
    Duration TIME,
    Movie_File BLOB,
    Ratings FLOAT CHECK (Ratings BETWEEN 0 AND 10),
    FOREIGN KEY (Movie_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Shows (
    Show_ID INT PRIMARY KEY,
    Ratings FLOAT,
    No_of_Seasons INT,
    FOREIGN KEY (Show_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Seasons (
    Season_ID INT PRIMARY KEY,
    ShowID INT NOT NULL,
    FOREIGN KEY (ShowID) REFERENCES Shows(Show_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Season_Details (
    Season_ID INT PRIMARY KEY,
    Description TEXT,
    Season_Number INT,
    Release_Year YEAR,
    No_of_Episodes TINYINT,
    FOREIGN KEY (Season_ID) REFERENCES Seasons(Season_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Episodes (
    Episode_No INT NOT NULL,
    Show_ID INT NOT NULL,
    Season_ID INT NOT NULL,
    Episode_File BLOB,
    Duration TIME,
    Air_Date DATE,
    Rating FLOAT,
    PRIMARY KEY (Episode_No, Show_ID, Season_ID), 
    FOREIGN KEY (Show_ID) REFERENCES Shows(Show_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Season_ID) REFERENCES Seasons(Season_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Actor (
    Actor_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INT,
    Country VARCHAR(50)
);

CREATE TABLE Review (
    Review_ID INT AUTO_INCREMENT PRIMARY KEY,
    Account_ID INT NOT NULL,
    Content_ID INT NOT NULL,
    Description TEXT,
    Rating FLOAT,
    Review_Date DATE,
    FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Content_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
); 

CREATE TABLE WatchList (
    AccountID INT NOT NULL,
    Content_ID INT NOT NULL,
    PRIMARY KEY (AccountID, Content_ID),
    FOREIGN KEY (AccountID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Content_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Account_Preferred_Languages (
    Account_ID INT NOT NULL,
    Preferred_Language VARCHAR(50),
    PRIMARY KEY (Account_ID, Preferred_Language),
    FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Account_Followers (
    Account_ID INT NOT NULL,
    Follower_ID INT NOT NULL,
    PRIMARY KEY (Account_ID, Follower_ID),
    FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Follower_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE 
);

CREATE TABLE Account_Following (
    Account_ID INT NOT NULL,
    Following_ID INT NOT NULL,
    PRIMARY KEY (Account_ID, Following_ID),
    FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Following_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE 
);

CREATE TABLE Account_Likes (
    Account_ID INT NOT NULL,
    Liked_Content_ID INT NOT NULL,
    PRIMARY KEY (Account_ID, Liked_Content_ID),
    FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Liked_Content_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Account_Watch_History (
    Account_ID INT NOT NULL,
    Watched_Content_ID INT NOT NULL,
    Duration_Watched TIME,
    Date_of_Watch_Start DATE,
    No_of_Times_Watched INT,
    PRIMARY KEY (Account_ID, Watched_Content_ID),
    FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Watched_Content_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Content_Genre (
    Content_ID INT NOT NULL,
    Content_Genre VARCHAR(50),
    PRIMARY KEY (Content_ID, Content_Genre),
    FOREIGN KEY (Content_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Content_Languages (
    Content_ID INT NOT NULL,
    Content_Language VARCHAR(50),
    PRIMARY KEY (Content_ID, Content_Language),
    FOREIGN KEY (Content_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Content_Actor (
    Content_ID INT NOT NULL,
    Actor_ID INT NOT NULL,
    Role VARCHAR(100),
    PRIMARY KEY (Content_ID, Actor_ID),
    FOREIGN KEY (Content_ID) REFERENCES Content(Content_ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (Actor_ID) REFERENCES Actor(Actor_ID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Subscription (
    SubscriptionID INT PRIMARY KEY,
    AccountID INT NOT NULL,
    First_Date_of_Subscription DATE,
    End_of_Subscription DATE,
    Last_Billing_Cycle DATE,
    Status ENUM('Active', 'Inactive', 'Cancelled') NOT NULL,
    FOREIGN KEY (AccountID) REFERENCES Account(Account_ID) ON UPDATE CASCADE ON DELETE CASCADE 

);


CREATE TABLE Mobile (
    SubscriptionID INT PRIMARY KEY,
    No_of_Devices TINYINT CHECK (No_of_Devices <= 1),
    Resolution VARCHAR(10) DEFAULT '480p',
    Price DECIMAL(6, 2) DEFAULT 149.00,
    FOREIGN KEY (SubscriptionID) REFERENCES Subscription(SubscriptionID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Basic (
    SubscriptionID INT PRIMARY KEY,
    No_of_Devices TINYINT CHECK (No_of_Devices <= 1),
    Resolution VARCHAR(10) DEFAULT '720p',
    Price DECIMAL(6, 2) DEFAULT 199.00,
    FOREIGN KEY (SubscriptionID) REFERENCES Subscription(SubscriptionID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Standard (
    SubscriptionID INT PRIMARY KEY,
    No_of_Devices TINYINT CHECK (No_of_Devices <= 2),
    Resolution VARCHAR(10) DEFAULT '1080p',
    Price DECIMAL(6, 2) DEFAULT 499.00,
    FOREIGN KEY (SubscriptionID) REFERENCES Subscription(SubscriptionID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Premium (
    SubscriptionID INT PRIMARY KEY,
    No_of_Devices TINYINT CHECK (No_of_Devices <= 4),
    Resolution VARCHAR(10) DEFAULT '4K',
    Price DECIMAL(6, 2) DEFAULT 599.00,
    FOREIGN KEY (SubscriptionID) REFERENCES Subscription(SubscriptionID) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Bank Details
INSERT INTO Bank_Details (Bank_Account_No, Bank_Name, Bank_Branch_Code) 
VALUES 
('1234567890', 'Bank of Example', 'BOE001'),
('0987654321', 'Global Bank', 'GB002'),
('1122334455', 'World Savings', 'WS003'),
('2233445566', 'National Trust', 'NT004'),
('3344556677', 'Credit Union', 'CU005'),
('4835556677', 'Credit Union', 'CU005'),
('7788990011', 'Bank of Example', 'BOE001'),
('8899001122', 'Global Bank', 'GB002'),
('9900112233', 'World Savings', 'WS003'),
('0011223344', 'National Trust', 'NT004'),
('6677889900' , 'statee bank' , 'BC---5');
-- Account
INSERT INTO Account (Name, Email, Password, Date_of_Birth, Account_Type, Date_of_First_Access, Country, No_of_Active_Devices, Bank_Account_No) 
VALUES
('Alice Johnson', 'alice@example.com', 'password123', '1990-05-15', 'General', '2023-01-01', 'USA', 2, '1234567890'),
('Bob Smith', 'bob@example.com', 'password456', '1985-09-21', 'General', '2023-02-15', 'Canada', 1, '0987654321'),
('Charlie Brown', 'charlie@example.com', 'password789', '1995-03-10', 'Kids', '2023-03-20', 'UK', 1, '1122334455'),
('Dana White', 'dana@example.com', 'password321', '1980-07-22', 'General', '2023-04-01', 'Australia', 3, '2233445566'),
('Eve Adams', 'eve@example.com', 'password654', '2000-12-30', 'Kids', '2023-05-10', 'India', 2, '3344556677'),
('Ken Adams', 'ken@example.com', 'password654', '2000-12-23', 'General', '2023-05-12', 'Bihar', 2, '4835556677');
INSERT INTO Account (Name, Email, Password, Date_of_Birth, Account_Type, Date_of_First_Access, Country, No_of_Active_Devices, Bank_Account_No) 
VALUES
('Grace Lee', 'grace@example.com', 'password654', '1992-08-14', 'General', '2023-07-15', 'Canada', 2, '6677889900'),
('Hank Green', 'hank@example.com', 'password321', '1988-02-25', 'Kids', '2023-08-20', 'UK', 1, '7788990011'),
('Ivy Brown', 'ivy@example.com', 'password123', '1999-04-30', 'General', '2023-09-01', 'Australia', 3, '8899001122'),
('Jack Black', 'jack@example.com', 'password456', '1983-12-12', 'Kids', '2023-10-10', 'India', 2, '9900112233'),
('Karen White', 'karen@example.com', 'password789', '1996-06-18', 'General', '2023-11-05', 'Bihar', 2, '0011223344');
-- Content
-- Populate Content Table with Movies
INSERT INTO Content (Content_ID, Title, Description, Country_of_Origin, Avg_Rating)
VALUES
(1, 'The Great Adventure', 'An epic journey across uncharted territories.', 'USA', 8.5),
(2, 'Comedy Chaos', 'A hilarious movie full of twists and turns.', 'Canada', 7.8),
(3, 'Romantic Rendezvous', 'A heartfelt love story spanning continents.', 'France', 8.9),
(4, 'The Galactic Wars', 'A sci-fi blockbuster about interstellar conflicts.', 'USA', 8.3),
(5, 'Nature’s Fury', 'A gripping documentary about natural disasters.', 'Australia', 7.5),
(6, 'The Hidden Truth', 'A thought-provoking mystery movie.', 'UK', 8.1),
(7, 'The Last Kingdom', 'A historical drama depicting a medieval empire.', 'India', 8.7),
(8, 'Eternal Love', 'A timeless love story of two souls.', 'Italy', 8.0),
(9, 'Cosmic Encounters', 'A space exploration movie with stunning visuals.', 'Germany', 8.4),
(10, 'The Final Heist', 'A high-stakes heist thriller.', 'USA', 8.6);

-- Populate Content Table with Shows
INSERT INTO Content (Content_ID, Title, Description, Country_of_Origin, Avg_Rating)
VALUES
(11, 'Mystery Manor', 'A suspenseful series unraveling the secrets of a haunted mansion.', 'UK', 9.0),
(12, 'The Detective’s Diary', 'A thrilling crime series with unexpected plot twists.', 'Germany', 8.5),
(13, 'The Last Stand', 'An action-packed series set in a post-apocalyptic world.', 'India', 8.0),
(14, 'Culinary Chronicles', 'A delightful show exploring cuisines worldwide.', 'Italy', 7.8),
(15, 'Legends of Mythica', 'A fantasy series based on ancient myths.', 'Japan', 9.2),
(16, 'Tech Titans', 'A series diving into the world of tech entrepreneurs.', 'USA', 8.8),
(17, 'World at War', 'A gripping war documentary series.', 'Canada', 9.1),
(18, 'The Comedy Club', 'A sitcom about the lives of stand-up comedians.', 'USA', 7.9),
(19, 'Into the Wild', 'A nature documentary exploring wildlife.', 'Australia', 8.3),
(20, 'Chasing Shadows', 'A psychological thriller uncovering dark secrets.', 'France', 8.6);

-- Populate Movies Table
INSERT INTO Movies (Movie_ID, Release_Year, Duration, Ratings)
VALUES
(1, 2020, '02:15:00', 8.5),
(3, 2019, '01:50:00', 7.8),
(5, 2021, '02:30:00', 8.9),
(7, 2018, '02:00:00', 8.3),
(9, 2022, '01:45:00', 7.5),
(11, 2019, '02:10:00', 8.1),
(13, 2020, '02:20:00', 8.7),
(15, 2021, '02:00:00', 8.0),
(17, 2023, '01:55:00', 8.4),
(19, 2023, '02:30:00', 8.6);
-- Populate Shows Table
INSERT INTO Shows (Show_ID, Ratings, No_of_Seasons)
VALUES
(2, 9.0, 3),
(4, 8.5, 2),
(6, 8.0, 1),
(8, 7.8, 4),
(10, 9.2, 3),
(12, 8.8, 2),
(14, 9.1, 1),
(16, 7.9, 5),
(18, 8.3, 3),
(20, 8.6, 2);

-- Seasons
-- Populate Seasons Table
INSERT INTO Seasons (Season_ID, ShowID)
VALUES
(1, 2), -- Mystery Manor
(2, 2),
(3, 2),
(4, 4), -- The Detective's Diary
(5, 4),
(6, 6), -- The Last Stand
(7, 8), -- Culinary Chronicles
(8, 8),
(9, 8),
(10, 8),
(11, 10), -- Legends of Mythica
(12, 10),
(13, 10);


-- Populate Season_Details Table
INSERT INTO Season_Details (Season_ID, Description, Season_Number, Release_Year, No_of_Episodes)
VALUES
(1, 'Introduction to the haunted mansion.', 1, 2020, 10),
(2, 'The mystery deepens with new discoveries.', 2, 2021, 8),
(3, 'A thrilling conclusion to the series.', 3, 2022, 9),
(4, 'A detective unravels a complex case.', 1, 2019, 7),
(5, 'New mysteries challenge the detective.', 2, 2020, 6),
(6, 'Survivors navigate a post-apocalyptic world.', 1, 2021, 12),
(7, 'Exploring Italian cuisine.', 1, 2018, 8),
(8, 'Exploring French cuisine.', 2, 2019, 7),
(9, 'Exploring Indian cuisine.', 3, 2020, 8),
(10, 'Exploring global cuisines.', 4, 2021, 9),
(11, 'A legendary heros origin.', 1, 2021, 10),
(12, 'The heros journey begins.', 2, 2022, 9),
(13, 'A grand finale to the saga.', 3, 2023, 8);


-- Populate Episodes Table
INSERT INTO Episodes (Episode_No, Show_ID, Season_ID, Duration, Air_Date, Rating)
VALUES

(1, 2, 1, '00:45:00', '2020-01-15', 8.9),
(2, 2, 1, '00:50:00', '2020-01-22', 8.8),
(3, 2, 1, '00:40:00', '2020-01-29', 9.0),

(1, 2, 2, '00:48:00', '2021-02-15', 9.1),
(2, 2, 3, '00:52:00', '2021-02-22', 9.0),

(1, 10, 11, '00:30:00', '2018-03-01', 7.8),
(2, 10, 12, '00:28:00', '2018-03-08', 8.0),
(3, 10, 11, '00:35:00', '2018-03-15', 7.9),
(4, 10, 13, '00:32:00', '2018-03-22', 8.1),
(5, 10, 12, '00:33:00', '2018-03-29', 7.7),
(6, 10, 13, '00:31:00', '2018-04-05', 7.9),
(7, 10, 11, '00:29:00', '2018-04-12', 8.0),
(8, 10, 11, '00:34:00', '2018-04-19', 7.8),

(1, 8, 7, '00:55:00', '2021-04-10', 9.2),
(2,  8, 7, '00:50:00', '2021-04-17', 9.1),
(3, 8, 7, '00:53:00', '2021-04-24', 9.3);

-- Actor
INSERT INTO Actor (Actor_ID, Name, Age, Country) 
VALUES 
(1, 'Chris Actor', 40, 'USA'),
(2, 'Emma Actress', 35, 'UK'),
(3, 'Liam Performer', 29, 'Australia'),
(4, 'Sophia Star', 32, 'India'),
(5, 'James Actor', 45, 'Canada'),
(6, 'Raj Actor', 40, 'India'),
(7, 'Sara Actress', 35, 'USA'),
(8, 'Rahul Performer', 29, 'India'),
(9, 'Katie Star', 32, 'Canada'),
(10, 'John Actor', 45, 'UK');

-- Review
INSERT INTO Review (Account_ID, Content_ID, Description, Rating, Review_Date) 
VALUES 
(1, 1, 'Amazing movie!', 9.0, '2023-01-05'),
(2, 2, 'Loved the show!', 8.8, '2023-02-20'),
(3, 3, 'Very funny!', 8.0, '2023-03-25'),
(4, 4, 'Great sci-fi tale.', 8.7, '2023-04-15'),
(5, 5, 'Interesting mystery.', 8.5, '2023-05-05'),
(1, 6, 'Great movie!', 9.0, '2023-06-05'),
(7, 7, 'Loved the show!', 8.8, '2023-07-20'),
(8, 8, 'Very funny!', 8.0, '2023-08-25'),
(1, 9, 'Great sci-fi tale.', 8.7, '2023-09-15'),
(10, 10, 'Interesting mystery.', 8.5, '2023-10-05');

-- WatchList
INSERT INTO WatchList (AccountID, Content_ID) 
VALUES 
(1, 1), 
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 6),
(1, 7),
(7, 8),
(1, 9),
(10, 10),
(10, 11),
(10, 12),
(10, 13),
(7,9);

-- Account Preferred Languages
INSERT INTO Account_Preferred_Languages (Account_ID, Preferred_Language) 
VALUES 
(1, 'English'), 
(2, 'French'),
(3, 'Spanish'),
(4, 'Hindi'),
(5, 'German'),
(1, 'Italian'),
(7, 'Japanese'),
(8, 'Chinese'),
(1, 'Russian'),
(10, 'Korean'),
(10, 'Arabic'),
(10, 'Portuguese'),
(7, 'Dutch'),
(9, 'Swedish');

-- Account Followers
INSERT INTO Account_Followers (Account_ID, Follower_ID) 
VALUES 
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 1),
(1, 7),
(7, 8),
(8, 1),
(1, 10),
(10, 7),
(7, 9),
(9, 10);

-- Account Following
INSERT INTO Account_Following (Account_ID, Following_ID) 
VALUES 
(2,1),
(3,2),
(7,1),
(10,1),
(4,3),
(5,4),
(1,5),
(8,7),
(1,8),
(7,10),
(9,7),
(10,9);

-- Account Likes
INSERT INTO Account_Likes (Account_ID, Liked_Content_ID) 
VALUES 
(1, 1), 
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(1, 6),
(7, 7),
(8, 8),
(1, 9),
(10, 10),
(10, 11),
(10, 12),
(10, 13),
(7, 9);


-- Account Watch History
INSERT INTO Account_Watch_History (Account_ID, Watched_Content_ID, Duration_Watched, Date_of_Watch_Start, No_of_Times_Watched) 
VALUES 
(1, 1, '01:45:00', '2023-01-06', 1),
(2, 2, '02:00:00', '2023-02-21', 2),
(3, 3, '01:30:00', '2023-03-22', 1),
(4, 4, '01:50:00', '2023-04-12', 3),
(5, 5, '01:40:00', '2023-05-11', 2),
(1, 6, '01:45:00', '2023-06-06', 1),
(7, 7, '02:00:00', '2023-07-21', 2),
(8, 8, '01:30:00', '2023-08-26', 1),
(1, 9, '01:50:00', '2023-09-16', 3),
(10, 10, '01:40:00', '2023-10-06', 2),
(10, 11, '01:45:00', '2023-11-06', 1),
(10, 12, '02:00:00', '2023-12-21', 2),
(10, 13, '01:30:00', '2024-01-26', 1),
(7, 9, '01:50:00', '2024-02-16', 3);

-- Content Genre
INSERT INTO Content_Genre (Content_ID, Content_Genre) 
VALUES 
(1, 'Adventure'), 
(2, 'Drama'),
(3, 'Comedy'),
(4, 'Sci-Fi'),
(5, 'Mystery'),
(6, 'Thriller'),
(7, 'Action'),
(8, 'Romance'),
(9, 'Documentary'),
(10, 'Crime'),
(1,'Thriller');



-- Content Languages
INSERT INTO Content_Languages (Content_ID, Content_Language) 
VALUES 
(1, 'English'), 
(2, 'French'),
(3, 'Spanish'),
(4, 'Hindi'),
(5, 'German'),
(6, 'Italian'),
(7, 'Japanese'),
(8, 'Chinese'),
(9, 'Russian'),
(10, 'Korean'),
(10, 'Arabic'),
(10, 'Portuguese'),
(7, 'Dutch'),
(9, 'Swedish');

-- Content Actor
INSERT INTO Content_Actor (Content_ID, Actor_ID, Role) 
VALUES 
(1, 1, 'Hero'), 
(2, 2, 'Lead Actress'),
(3, 3, 'Comedian'),
(4, 4, 'Scientist'),
(5, 5, 'Detective'),
(1,3,'receptionist'),
(7, 7, 'Heroine'),
(8, 8, 'Lead Actor'),
(1, 9, 'Villain'),
(10, 10, 'Sidekick'),
(10, 2, 'Hero'),
(10, 9, 'Lead Actress'),
(10, 6, 'Comedian'),
(7, 4, 'Scientist');

-- Subscription
INSERT INTO Subscription (SubscriptionID, AccountID, First_Date_of_Subscription, End_of_Subscription, Last_Billing_Cycle, Status) 
VALUES 
(1, 1, '2023-01-01', '2024-01-01', '2023-12-01', 'Active'),
(2, 2, '2023-02-15', '2024-02-15', '2023-11-15', 'Active'),
(3, 3, '2023-03-20', '2024-03-20', '2023-12-20', 'Active'),
(4, 4, '2023-04-10', '2024-04-10', '2023-12-10', 'Cancelled'),
(5, 5, '2023-05-05', '2024-05-05', '2023-12-05', 'Active'),
(6, 6, '2023-06-05', '2024-06-05', '2023-12-05', 'Active'),
(7, 7, '2023-07-20', '2024-07-20', '2023-12-20', 'Active'),
(8, 8, '2023-08-25', '2024-08-25', '2023-12-25', 'Active'),
(9, 9, '2023-09-15', '2024-12-28', '2023-12-15', 'Active'),
(10, 10, '2023-10-05', '2024-11-28', '2023-12-05', 'Active');


-- Populate Mobile Table
INSERT INTO Mobile (SubscriptionID, No_of_Devices, Resolution, Price)
VALUES
(1, 1, '480p', 149.00),
(2, 1, '480p', 149.00),
(3, 1, '480p', 149.00);


-- Populate Basic Table
INSERT INTO Basic (SubscriptionID, No_of_Devices, Resolution, Price)
VALUES
(5, 1, '720p', 199.00),
(6, 1, '720p', 199.00);

-- Populate Standard Table
INSERT INTO Standard (SubscriptionID, No_of_Devices, Resolution, Price)
VALUES
(9, 2, '1080p', 499.00),
(10, 2, '1080p', 499.00);

-- Populate Premium Table
INSERT INTO Premium (SubscriptionID, No_of_Devices, Resolution, Price)
VALUES
(7, 4, '4K', 599.00),
(8, 4, '4K', 599.00);

CREATE EVENT UpdateSubscriptionStatus
ON SCHEDULE EVERY 1 DAY
DO
    UPDATE Subscription
    SET Status = 'Inactive'
    WHERE End_of_Subscription < CURDATE();
