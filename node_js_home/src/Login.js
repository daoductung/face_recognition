import React from 'react';
import './scss/Login.scss';
import {Form, Input, Button, Checkbox} from 'antd';
import {UserOutlined, LockOutlined} from '@ant-design/icons';

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
			username: "",
			password: "",
			errors: {
				username: "",
				password: ""
			}
		}
    }

    onFinish = (e) => {
		e.preventDefault();
		const {onLogin} = this.props;
		let {username, password, errors} = this.state;
		errors = {
			username: "",
			password: ""
		}
		this.setState({errors});
		if(!username){
			errors.username = "Vui lòng nhập tài khoản!";
			this.setState({errors});
			return;
		}
		if(!password){
			errors.password = "Vui lòng nhập mật khẩu!";
			this.setState({errors});
			return;
		}
        onLogin(username, password);
    };

    render = () => {
		const {username, password, errors} = this.state;
        return (
            <div className="login">
            <div className="container">
                <header>HỆ THỐNG<br/>NHẬN DIỆN KHUÔN MẶT</header>
                <form onSubmit={this.onFinish}>
                    <div className="input-field">
                        <input value={username} onChange={e => this.setState({username: e.target.value})} type="text" placeholder="Tài khoản"/>
                    </div>
					<em className="required">{errors.username}</em>
                    <div className="input-field">
                        <input value={password} onChange={e => this.setState({password: e.target.value})} className="pswrd" type="password" placeholder="Mật khẩu"/>
                    </div>
					<em className="required">{errors.password}</em>
                    <div className="button">
                        <div className="inner"></div>
                        <button>ĐĂNG NHẬP</button>
                    </div>
                </form>
            </div>
			</div>
        );
    }
}

export default Login;
