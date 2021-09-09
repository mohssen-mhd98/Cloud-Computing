import os

from flask import Flask, jsonify, request, make_response, redirect, url_for
from functools import wraps
import jwt
import datetime
import command_handler as ch

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['authorization']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/protected')
@token_required
def protected(current_user):
    # print('-------------------------------------------------------------------')
    # print(type(current_user))
    content = request.get_json(silent=True)
    header = request.headers.get('Content-Type')
    content_header = header.split(';')[0]
    print(content_header)
    print(content)
    if content:
        if content['command'] == 'status':
            if len(content) > 1:
                machine_name = content['vmName']
                machine_state = ch.get_state(machine_name)
                print(machine_state)
                content.update({'status:': machine_state})
                return jsonify(content)
            else:
                details = ch.get_states()
                content.update({'details': details})
                # print('------------------------------------')
                # print(content)
                return jsonify(content)

        elif content['command'] == 'on':
            machine_name = content['vmName']
            ch.start_machine(machine_name)
            content.update({'status': 'powering on'})
            return jsonify(content)

        elif content['command'] == 'off':
            machine_name = content['vmName']
            ch.shutdown_machine(machine_name)
            content.update({'status': 'powering off'})
            return jsonify(content)

        elif content['command'] == 'setting':
            vm_name = content['vmName']
            cpu = content['cpu']
            ram = content['ram']
            ch.modify_cores(vm_name, cpu)
            ch.modify_memory(vm_name, ram)

            content.update({'status': 'OK'})
            return jsonify(content)

        elif content['command'] == 'clone':
            src_vm_name = content['sourceVmName']
            dst_vm_name = content['destVmName']
            ch.clone_machine(src_vm_name, dst_vm_name)
            content.update({'status': 'OK'})
            return jsonify(content)

        elif content['command'] == 'delete':
            vm_name = content['vmName']
            ch.delete_machine(vm_name)
            content.update({'status': 'OK'})
            return jsonify(content)

        elif content['command'] == 'execute':
            if current_user == 'admin':
                vm_name = content['vmName']
                command = content['input']
                res = ch.execute_command(vm_name, command)
                content.update({'response': res})
                return jsonify(content)
            else:
                return jsonify({'PERMISSION DENIED': 'You can not run admin commands!'})

        elif content['command'] == 'transfer':
            origin_vm = content['originVM']
            origin_path = content['originPath']
            dst_vm = content['destVM']
            dst_path = content['destPath']
            f_name = origin_path.split('/')
            f_name = f_name[-1]
            middle_path = 'D:\\' + f_name
            ch.transfer_file(origin_vm, dst_vm, origin_path, middle_path, dst_path)
            content.update({'status': 'OK'})

            return jsonify(content)

    elif content_header == 'multipart/form-data':
        # vm_name = content['vmName']
        # src_path = content['source-directory']
        # dest_path = content['dest-directory']
        store_path = 'C:\\Users\\AVAJANG\\Desktop'

        file_name = request.files['file'].filename
        dest_path = request.form['dest-directory']
        target_machine = request.form['target-machine']

        f = request.files["file"]
        f.save(os.path.join(store_path, f.filename))
        src_path = store_path + "\\" + file_name
        ch.upload_file(target_machine, dest_path, src_path)
        content_tmp = {}
        content_tmp.update({'vmName': target_machine, 'status': 'File copied'})
        return jsonify(content_tmp)

    return jsonify({'message': 'This is only available for people with valid tokens.'})


@app.route('/login')
def login():
    # request.authorization = None
    auth = request.authorization
    if auth and auth.username == 'admin':
        if auth.password == 's1':
            token = jwt.encode({'authorization': auth.username,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                               app.config['SECRET_KEY'], algorithm="HS256")

            return jsonify({'token': token})
    elif auth and auth.username == 'User1':
        if auth.password == 's2':
            token = jwt.encode({'authorization': auth.username,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                               app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'token': token})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/')
def root():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
