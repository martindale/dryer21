from flask import Flask
from flask import make_response, redirect, render_template, request, json, url_for
jsonify = json.jsonify

app = Flask(__name__)
# Restrict uploading files larger than 10kB. FIXME: Set to size of bond in the future.
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024

@app.route('/')
@app.route('/index')
def index():
	return render_template('redeemer.html')

@app.route('/bond', methods=['GET', 'POST'])
def redeem_bond():
	if request.method == 'GET':
		return redirect(url_for('index'))
	bond_file = request.files['bond_file']
	if not bond_file:
		return bond_error('No bond supplied!')
	bond = bond_file.read()
	if not bond:
		return bond_error('Bond file empty!')
	to_addr = request.form.get('to_addr', None)
	if not to_addr:
		return bond_error('No destination bitcoin address supplied!')
	return render_template('bond_success.html', to_addr=to_addr)

def bond_error(err_msg=None):
	return render_template('bond_error.html', err_msg=err_msg)

@app.errorhandler(413)
def request_entity_too_large(error):
	return bond_error('The file you tried to upload was too large!'), 413

if __name__ == '__main__':
	app.run(port=9002)