### Name:
    Ritu Raj

### Ip Address
    67.205.136.57

### Phpmyadmin Link
    http://67.205.136.57/phpmyadmin

## Table Create statements

#### gift_options.sql

```sql
CREATE TABLE IF NOT EXISTS `gift_options` (
       	`allowGiftWrap` TINYINT(1) NOT NULL,
       	`allowGiftMessage` TINYINT(1) NOT NULL,
       	`allowGiftReceipt` TINYINT(1) NOT NULL,
       	primary key(allowGiftReceipt)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### image_entities.sql

```sql
CREATE TABLE IF NOT EXISTS `image_entities` (
       	`thumbnailImage` varchar(149) NOT NULL,
       	`mediumImage` varchar(149) NOT NULL,
       	`largeImage` varchar(149) NOT NULL,
       	`entityType` varchar(9) NOT NULL,
       	primary key(thumbnailImage,mediumImage,largeImage,entityType)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### market_place_price.sql

```sql
CREATE TABLE IF NOT EXISTS `market_place_price` (
       	`price` float(6) NOT NULL,
       	`sellerInfo` varchar(44) NOT NULL,
       	`standardShipRate` float(6) NOT NULL,
       	`twoThreeDayShippingRate` float(6) NOT NULL,
       	`availableOnline` tinyint(1) NOT NULL,
       	`clearance` tinyint(1) NOT NULL,
       	`offerType` varchar(16) NOT NULL,
       	primary key(price,sellerInfo,availableOnline)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```

#### products.sql

```sql
CREATE TABLE IF NOT EXISTS `products` (
       	`itemId` int(9) NOT NULL,
       	`parentItemId` int(9) NOT NULL,
       	`name` varchar(200) NOT NULL,
       	`salePrice` float(6) NOT NULL,
       	`upc` varchar(12) NOT NULL,
       	`categoryPath` varchar(123)NOT NULL,
       	`shortDescription` varchar(1112) NOT NULL,
       	`longDescription` varchar(5540)NOT NULL,
       	`brandName` varchar(36)NOT NULL,
       	`thumbnailImage` varchar(149) NOT NULL,
       	`mediumImage` varchar(149) NOT NULL,
       	`largeImage` varchar(149) NOT NULL,
       	`productTrackingUrl` varchar(416) NOT NULL,
       	`modelNumber` varchar(53) NOT NULL,
       	`productUrl` varchar(345) NOT NULL,
       	`categoryNode` varchar(23) NOT NULL,
       	`stock` varchar(13) NOT NULL,
       	`addToCartUrl` varchar(221) NOT NULL,
       	`affiliateAddToCartUrl` varchar(296) NOT NULL,
       	`offerType` varchar(16) NOT NULL,
       	`msrp` float(6) NOT NULL,
       	`standardShipRate` float(6) NOT NULL,
       	`color` varchar(10) NOT NULL,
       	`customerRating` varchar(5) NOT NULL,
       	`numReviews`int(5) NOT NULL,
       	`customerRatingImage` varchar(48) NOT NULL,
       	`maxItemsInOrder` int(6) NOT NULL,
       	`size` varchar(49) NOT NULL,
       	`sellerInfo` varchar(44) NOT NULL,
       	`age` varchar(14) NOT NULL,
       	`gender` varchar(6) NOT NULL,
       	`isbn` varchar(13) NOT NULL,
       	`preOrderShipsOn` varchar(19) NOT NULL,
       	PRIMARY KEY(itemId,parentItemId,name,upc,brandName,modelNumber,color,sellerInfo,isbn)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```
