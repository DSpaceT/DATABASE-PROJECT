CREATE TABLE IF NOT EXISTS School(
    school_id INT AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL UNIQUE,
    city VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    address VARCHAR(40) NOT NULL,
    total_borrows INT NOT NULL,
    PRIMARY KEY (school_id)
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Phone(
    phone_id INT AUTO_INCREMENT,
    school_id INT,
    phone INT(10),
    PRIMARY KEY (phone_id),
    CONSTRAINT fk_Phone_school
        FOREIGN KEY (school_id)
        REFERENCES School (school_id)
        ON UPDATE CASCADE 
        ON DELETE RESTRICT
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS App_user(
    user_id INT AUTO_INCREMENT,
    school_id INT,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    age INT UNSIGNED,
    type VARCHAR(40),
    card INT,
    admin_id INT,
    approved BIT,
    PRIMARY KEY (user_id),
    CONSTRAINT fk_App_user_school
        FOREIGN KEY (school_id)
        REFERENCES School (school_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Authentication(
    auth_id INT AUTO_INCREMENT,
    user_id INT,
    username VARCHAR(40) NOT NULL UNIQUE,
    password VARCHAR(40) NOT NULL,
    PRIMARY KEY (auth_id),
    CONSTRAINT fk_Authentication_App_user
        FOREIGN KEY (user_id)
        REFERENCES App_user (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Books(
    isbn INT,
    page_count INT UNSIGNED,
    publisher VARCHAR(40),
    title VARCHAR(40) NOT NULL,
    summary VARCHAR(40),
    cover_path VARCHAR(60),
    PRIMARY KEY (isbn)
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Categories(
    category_id INT AUTO_INCREMENT,
    isbn INT,
    category VARCHAR(40) NOT NULL,
    PRIMARY KEY (category_id),
    CONSTRAINT fk_Categories_Books
        FOREIGN KEY (isbn)
        REFERENCES Books (isbn)
        ON UPDATE CASCADE 
        ON DELETE CASCADE
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Keywords(
    keyword_id INT AUTO_INCREMENT,
    isbn INT,
    keyword VARCHAR(40) NOT NULL,
    PRIMARY KEY (keyword_id),
    CONSTRAINT fk_Keywords_Books
        FOREIGN KEY (isbn)
        REFERENCES Books (isbn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Authors(
    author_id INT AUTO_INCREMENT,
    isbn INT,
    first_name VARCHAR(40),
    last_name VARCHAR(40),
    PRIMARY KEY (author_id),
    CONSTRAINT fk_Authors_Books
        FOREIGN KEY (isbn)
        REFERENCES Books (isbn)
        ON UPDATE CASCADE 
        ON DELETE CASCADE
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Stores(
    store_id INT AUTO_INCREMENT,
    school_id INT,
    isbn INT,
    copies INT NOT NULL,
    PRIMARY KEY (store_id),
    CONSTRAINT fk_Stores_Books
        FOREIGN KEY (isbn)
        REFERENCES Books (isbn)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_Stores_School
        FOREIGN KEY (school_id)
        REFERENCES School (school_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Borrow(
    borrow_id INT AUTO_INCREMENT,
    isbn INT,
    user_id INt,
    return_date DATE NOT NULL,
    acquire_date DATE NOT NULL,
    PRIMARY KEY (borrow_id),
    CONSTRAINT fk_Borrow_Books
        FOREIGN KEY (isbn)
        REFERENCES Books (isbn)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    CONSTRAINT fk_Borrow_App_user
        FOREIGN KEY (user_id)
        REFERENCES App_user (user_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
)ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS Review (
        review_id INT AUTO_INCREMENT,
        date_of_review DATE NOT NULL,
        score INT UNSIGNED,
        description VARCHAR(500),
        isbn INT,
        user_id INT,
        PRIMARY KEY (review_id),
        CONSTRAINT fk_Review_Books
          FOREIGN KEY (isbn)
          REFERENCES Books (isbn)
          ON UPDATE CASCADE
          ON DELETE CASCADE,
        CONSTRAINT fk_Review_App_user
          FOREIGN KEY (user_id)
          REFERENCES App_user (user_id)
          ON UPDATE CASCADE
          ON DELETE CASCADE)
ENGINE = InnoDB;            

CREATE TABLE IF NOT EXISTS Request(
        request_id INT AUTO_INCREMENT,
        date_of_request DATE NOT NULL,
        isbn INT,
        user_id INT,
        PRIMARY KEY (request_id),
        CONSTRAINT fk_Request_Books
          FOREIGN KEY (isbn)
          REFERENCES Books (isbn)
          ON UPDATE CASCADE
          ON DELETE CASCADE,
        CONSTRAINT fk_Request_App_user
          FOREIGN KEY (user_id)
          REFERENCES App_user (user_id)
          ON UPDATE CASCADE
          ON DELETE CASCADE)
ENGINE = InnoDB;