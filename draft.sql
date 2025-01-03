-- Let me insert the admin user (me) as the first user!
INSERT INTO "users"("username", "password")
VALUES ('admin', '123');

-- Insert a wallet for the admin user.
INSERT INTO "wallets"("name", "amount", "user_id")
VALUES (
    'myWallet',
    500,
    (SELECT "id" FROM "users"
    WHERE "id" = 1)
);

-- Lets create another wallet for testing for admin user
INSERT INTO "wallets"("name", "amount", "user_id")
VALUES (
    'jobWallet',
    1000,
    (SELECT "id" FROM "users"
    WHERE "id" = 1)
);

-- Lets select the user's wallets and display them!
SELECT "name", "amount" FROM "wallets"
WHERE "user_id" = "1"

-- What if we want to delete?
DELETE FROM "users"
WHERE "username" = "admin";
-- No need to worry about the wallet, it auto deletes because of cascading!


-- May create a view to view  wallets
SELECT "username", "name" FROM "users"
JOIN "wallets" ON "wallets"."user_id" = "users"."id";

-- Let's insert a wallet
INSERT INTO "wallets"("name", "amount", "user_id")
VALUES (
    'jobWallet',
    1000,
    (SELECT "id" FROM "users"
    WHERE "id" = 2)
);

-- Delete a wallet

DELETE FROM "wallets"
WHERE "name" = ?
AND "user_id" = ?;

-- Update a password
UPDATE "users"
SET "password" = ?
WHERE "user_id" = ?;

-- MAYBE IN THE TRANSACTIONS TABLE YOU CAN LET USER ADD A NOTE, Just like the wallet app!


-- Update a username
UPDATE "users"
SET "username" = ?
WHERE "id" = ?;

-- Delete an account
DELETE FROM "users"
WHERE "id" = ?;

-- Deposit into a wallet!

UPDATE "wallets"
SET "amount" =

-- Old deleted schema tables:

-- Lets keep track of each deposit, withdraw!
CREATE TABLE "transactions" (
    "id" INTEGER, -- Id of that transaction
    "type" TEXT NOT NULL CHECK("type" IN ('Deposit', 'Withdraw')),
    "amount" NUMERIC NOT NULL, -- Amount based on the type
    "wallet_id" INTEGER, -- From which wallet?
    "user_id" INTEGER, -- A User can do more than one transactions
    PRIMARY KEY("id"),
    FOREIGN KEY("wallet_id") REFERENCES "wallets"("id"),
    FOREIGN KEY("user_id") REFERENCES "users"("id")
);

-- Lets not keep track of the transfer transaction in a seperate table!
CREATE TABLE "transfer_transaction" (
    "id" INTEGER, -- Id of that transfer
    "amount" NUMERIC NOT NULL,
    "from_user_walletID" INTEGER, -- No need to track user id over here!
    "to_user_walletID" INTEGER,
    PRIMARY KEY("id"),
    FOREIGN KEY("from_user_walletID") REFERENCES "wallets"("id"),
    FOREIGN KEY("to_user_walletID") REFERENCES "wallets"("id")
);

-- Now time to optimize our queries using indexes
