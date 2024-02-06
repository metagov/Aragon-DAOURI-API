# Aragon DAO URI API Documentation
## 1. Endpoint: /fetch_aragon_daos/<network>
**Description:** Fetches a list of DAOs from the specified Aragon network.

**Method:** GET

**URL Structure:** /fetch_aragon_daos/<network>

**Path Parameter:** network - The network to fetch DAOs from. This is a part of the URL path.

**Available Network Options:**

- arbitrum: Aragon DAOs on Arbitrum Mainnet
- arbitrum-goerli: Aragon DAOs on Arbitrum Goerli Testnet
- base: Aragon DAOs on Base Mainnet
- base-goerli: Aragon DAOs on Base Goerli Testnet
- ethereum: Aragon DAOs on Ethereum Mainnet
- goerli: Aragon DAOs on Goerli Testnet
- mumbai: Aragon DAOs on Mumbai Testnet (Polygon)
- polygon: Aragon DAOs on Polygon Mainnet
- sepolia: Aragon DAOs on Sepolia Testnet

## 2. Endpoint: /aragon_dao/<network>/<dao_id>
**Description:** Fetches specific DAO details based on the network and DAO ID.

**Method:** GET

**URL Structure:** /aragon_dao/<network>/<dao_id>

**Path Parameters:**

- network: The network the DAO is on. Refer to the list of available networks above.
- dao_id: The unique identifier of the DAO. This is a part of the URL path. Ex: 0x02bbc496bebc9a06c239670cea663c43cead899f
