-- In this SQL file, write (and comment!) the schema of your database, including the CREATE TABLE, CREATE INDEX, CREATE VIEW, etc. statements that compose it

-- So we're gonna visualize the idea of the bank accounts as the wallet app! So we're gonna create accounts
-- So am gonna add a password for each user, and in the python program make the user enter it, and if succesful make him enter!
-- Make sure to create a process to make a new user or delete!
CREATE TABLE "users" (
    "id" INTEGER, -- Id of the user
    "username" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    PRIMARY KEY("id")
);

-- Lets create wallets with a one to many relationships with users, where each other can have many wallets, but each
-- A wallet can have only one user! That means wallets CANNOT be shared! Each one is unique to each user!
-- Make sure to have a process that displays wallets of that user (if login was succesful)
-- Make sure to have a process to make a new wallet or delete!
CREATE TABLE "wallets" (
    "id" INTEGER, -- Id of that wallet
    "name" TEXT NOT NULL, -- Name of the wallet
    "amount" NUMERIC NOT NULL CHECK("amount" >= 0), -- amount in the wallet
    "user_id" INTEGER, -- So the user can be repeated
    PRIMARY KEY("id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id") ON DELETE CASCADE -- When a user is delete, wallets are deleted
);

CREATE INDEX "userName" ON "users"("username");
CREATE INDEX "userID_index" ON "wallets"("user_id");
