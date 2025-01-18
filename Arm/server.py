from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/players', methods=['GET'])
def get_players():
    players = [
        {
            'id': 1,
            'name': 'Player 1',
            'center': [100, 150],
            'direction': [2, 3],
            'score': 10
        },
        {
            'id': 2,
            'name': 'Player 2',
            'center': [200, 250],
            'direction': [-3, 2],
            'score': 20
        },
        {
            'id': 3,
            'name': 'Player 3',
            'center': [300, 350],
            'direction': [1, -1],
            'score': 15
        },
        {
            'id': 4,
            'name': 'Player 4',
            'center': [400, 450],
            'direction': [-2, -3],
            'score': 25
        },
        {
            'id': 5,
            'name': 'Player 5',
            'center': [500, 550],
            'direction': [0, -2],
            'score': 30
        },
        {
            'id': 6,
            'name': 'Player 6',
            'center': [600, 650],
            'direction': [3, -1],
            'score': 18
        },
        {
            'id': 7,
            'name': 'Player 7',
            'center': [700, 750],
            'direction': [-1, -2],
            'score': 22
        },
        {
            'id': 8,
            'name': 'Player 8',
            'center': [800, 850],
            'direction': [2, -3],
            'score': 12
        },
        {
            'id': 9,
            'name': 'Player 9',
            'center': [900, 950],
            'direction': [-3, -1],
            'score': 27
        },
        {
            'id': 10,
            'name': 'Player 10',
            'center': [1000, 1050],
            'direction': [1, -2],
            'score': 35
        }
    ]
    return jsonify({'players': players})

if __name__ == '__main__':
    app.run(debug=True)
