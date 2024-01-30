from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Dictionary of Aragon API endpoints
aragon_api_endpoints = {
    'arbitrum': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-arbitrum/version/v1.4.0/api',
    'arbitrum-goerli': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-arbitrumGoerli/version/v1.4.0/api',
    'base': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-baseMainnet/version/v1.4.0/api',
    'base-goerli': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-baseGoerli/version/v1.4.0/api',
    'ethereum': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-mainnet/version/v1.4.0/api',
    'goerli': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-goerli/version/v1.4.0/api',
    'mumbai': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-mumbai/version/v1.4.0/api',
    'polygon': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-polygon/version/v1.4.0/api',
    'sepolia': 'https://subgraph.satsuma-prod.com/qHR2wGfc5RLi6/aragon/osx-sepolia/version/v1.4.0/api',
}

def fetch_aragon_daos(network):
    # Check if the network is supported
    if network not in aragon_api_endpoints:
        return jsonify({"error": f"Network '{network}' not supported"}), 400

    # Aragon DAO API endpoint for the given network
    aragon_api_url = aragon_api_endpoints[network]

    # GraphQL query
    query = {
        "query": "{ daos { id daoURI metadata } }"
    }

    # Make request to Aragon API
    response = requests.post(aragon_api_url, json=query)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Aragon API"}), response.status_code

    daos = response.json()['data']['daos']

    # Process each DAO
    formatted_daos = []
    for dao in daos:
        # Extract CID from metadata IPFS link
        cid = dao['metadata'][7:] if dao['metadata'].startswith('ipfs://') else dao['metadata']
        metadata_url = f"https://ipfs.io/ipfs/{cid}"

        # Format the data
        formatted_dao = {
            "@context": "http://www.daostar.org/schemas",
            "type": "DAO",
            "name": dao['id'],
            "description": metadata_url,
            "membersURI": f"https://app.aragon.org/#/daos/{network}/{dao['id']}/community",
            "proposalsURI": f"https://app.aragon.org/#/daos/{network}/{dao['id']}/governance",
            "activityLogURI": f"https://app.aragon.org/#/daos/{network}/{dao['id']}/dashboard",
            "contractsRegistryURI": f"https://app.aragon.org/#/daos/{network}/{dao['id']}/settings"
        }
        formatted_daos.append(formatted_dao)

    return jsonify(formatted_daos)

# Dynamic route for each network
@app.route('/fetch_aragon_daos/<network>', methods=['GET'])
def fetch_aragon_daos_route(network):
    return fetch_aragon_daos(network)

def aragon_dao(network, dao_id):
    if network not in aragon_api_endpoints:
        return jsonify({"error": f"Network '{network}' not supported"}), 400

    aragon_api_url = aragon_api_endpoints[network]

    # Adjusted GraphQL query for specific DAO ID
    query = {
        "query": """
        query GetDAO($daoId: ID!) {
          dao(id: $daoId) {
            id
            daoURI
            metadata
          }
        }""",
        "variables": {"daoId": dao_id}
    }

    response = requests.post(aragon_api_url, json=query)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Aragon API"}), response.status_code

    dao_data = response.json().get('data', {}).get('dao')
    if not dao_data:
        return jsonify({"error": "DAO not found"}), 404

    # Extract CID from metadata IPFS link
    cid = dao_data['metadata'][7:] if dao_data['metadata'].startswith('ipfs://') else dao_data['metadata']
    metadata_url = f"https://ipfs.io/ipfs/{cid}"

    formatted_dao = {
        "@context": "http://www.daostar.org/schemas",
        "type": "DAO",
        "name": dao_id,
        "description": metadata_url,
        "membersURI": f"https://app.aragon.org/#/daos/{network}/{dao_id}/community",
        "proposalsURI": f"https://app.aragon.org/#/daos/{network}/{dao_id}/governance",
        "activityLogURI": f"https://app.aragon.org/#/daos/{network}/{dao_id}/dashboard",
        "contractsRegistryURI": f"https://app.aragon.org/#/daos/{network}/{dao_id}/settings"
    }

    return jsonify(formatted_dao)


@app.route('/aragon_dao/<network>/<dao_id>', methods=['GET'])
def aragon_dao_route(network, dao_id):
    if not network or not dao_id:
        return jsonify({"error": "Network and DAO ID parameters are required"}), 400
    return aragon_dao(network, dao_id)

@app.route('/', methods=['GET'])
def api_documentation():
    documentation = """
    <h1>Flask API Documentation</h1>

    <h2>1. Endpoint: /fetch_aragon_daos/&lt;network&gt;</h2>
    <p><strong>Description:</strong> Fetches a list of DAOs from the specified Aragon network.</p>
    <p><strong>Method:</strong> GET</p>
    <p><strong>URL Structure:</strong> /fetch_aragon_daos/&lt;network&gt;</p>
    <p><strong>Path Parameter:</strong> <code>network</code> - The network to fetch DAOs from. This is a part of the URL path.</p>
    <p><strong>Available Network Options:</strong></p>
    <ul>
        <li><code>arbitrum</code>: Aragon DAOs on Arbitrum Mainnet</li>
        <li><code>arbitrum-goerli</code>: Aragon DAOs on Arbitrum Goerli Testnet</li>
        <li><code>base</code>: Aragon DAOs on Base Mainnet</li>
        <li><code>base-goerli</code>: Aragon DAOs on Base Goerli Testnet</li>
        <li><code>ethereum</code>: Aragon DAOs on Ethereum Mainnet</li>
        <li><code>goerli</code>: Aragon DAOs on Goerli Testnet</li>
        <li><code>mumbai</code>: Aragon DAOs on Mumbai Testnet (Polygon)</li>
        <li><code>polygon</code>: Aragon DAOs on Polygon Mainnet</li>
        <li><code>sepolia</code>: Aragon DAOs on Sepolia Testnet</li>
    </ul>

    <h2>2. Endpoint: /aragon_dao/&lt;network&gt;/&lt;dao_id&gt;</h2>
    <p><strong>Description:</strong> Fetches specific DAO details based on the network and DAO ID.</p>
    <p><strong>Method:</strong> GET</p>
    <p><strong>URL Structure:</strong> /aragon_dao/&lt;network&gt;/&lt;dao_id&gt;</p>
    <p><strong>Path Parameters:</strong></p>
    <ul>
        <li><code>network</code>: The network the DAO is on. Refer to the list of available networks above.</li>
        <li><code>dao_id</code>: The unique identifier of the DAO. This is a part of the URL path. Ex: 0x02bbc496bebc9a06c239670cea663c43cead899f </li>
    </ul>
    """

    return documentation


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
