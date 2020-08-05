import React, { useEffect, useState } from 'react';
import './scss/App.scss';
import Login from './Login';
import { Modal , Form, Input, Button, Popconfirm, message, Space ,Spin, InputNumber, notification, DatePicker } from 'antd';
import { EditOutlined, DeleteOutlined, QuestionCircleOutlined, LoadingOutlined } from '@ant-design/icons';
import axios from 'axios';


class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      students:[
      ],
      student_report:[
      ],
      status_view: false,
      check_login: false,
      visible: false,
      post_image: true,
      get_information: true,
      isEdit: false,
      editData: {},
      is_capture:false,
      image_edit: "",
      fields: [],
      dataResult: true,
      is_detect: false,
      is_loading: false,
      is_loading_train: false,
      is_train: true,
      is_report: false,
      dateRanger: []
    }
    this.timer = null;
  }

  layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
  };
  tailLayout = {
    wrapperCol: { offset: 8, span: 16 },
  };
  
  onFinish = values => {
    const {students} = this.state;
    if (this.canvas){
      var data = this.canvas.toDataURL('image/jpg');
      values.image = data;
    }

    if(this.state.isEdit){
      // axios.post('http://127.0.0.1:9898/edit/'+this.state.editData.id, values).then((res) => {
      //   //
      //   this.setState({students, visible: false});
      // }).catch(err => {
      //   console.log(err)
      // });
      let existStudent = students.find((obj) => obj.id === this.state.editData.id);
      if(existStudent){
        // Object.keys(existStudent).map((key) => {
        //   if(values.hasOwnProperty(key)){
        //     existStudent[key] = values[key];
        //   }
        // });
        // this.setState({students, isEdit: false, visible: false, editData: {}});
        axios.post('http://127.0.0.1:9898/edit/'+ existStudent['id'], values).then((res) => {
          let std = [];
          fetch('http://127.0.0.1:9898/getAll').then(res => {
            return res.json();
            }).then(data => {
              std = data
              this.setState({students: std, isEdit: false, visible: false, editData: {}})
            });
        }).catch(err => {
          console.log(err)
        });
      }
    }else{
      axios.post('http://127.0.0.1:9898/add', values).then((res) => {
        students.push({
          id: res.data.data,
          ...values
        });
        
        this.setState({students, visible: false});
      }).catch(err => {
        console.log(err)
      });
    }
  };

  notification_func = (title, message) => {
    notification.open({
      message: title,
      description: message,
      onClick: () => {
        console.log('Notification Clicked!');
      },
    });
  }


  showAdd = () => {
    this.setState({
      editData: {},
      isEdit: false,
      visible: true,
      is_capture: false,
      image_edit: "",
      fields: []
    });
    navigator.mediaDevices.getUserMedia({video: true, audio: false}).then((stream) => {
      if (this.video){
        this.video.srcObject = stream;
        this.video.play();
      }
    });
  };

  showEdit = (item) => {
    let fields = [];
    Object.keys(item).map((key) => {
      fields.push({
        name: [key],
        value: item[key]
      })
    });
    console.log(item);
    this.setState({
      editData: item,
      isEdit: true,
      visible: true,
      is_capture: item.image ? true : false,
      image_edit: item.image,
      fields
    });
    navigator.mediaDevices.getUserMedia({video: true, audio: false}).then((stream) => {
      if (this.video){
        this.video.srcObject = stream;
        this.video.play();
      }
    });
  }

  handleDetect = () => {
    this.setState({is_detect: !this.state.is_detect, dataResult: !this.state.is_detect, is_loading : !this.state.is_loading})
    if (this.state.post_image && !this.state.is_detect) {
      this.autoCapture();
      this.post_image_result();
      this.setState({dataResult: false});
    }
  }

  handleViewReport = () => {
    this.setState({is_report: true, status_view: false})
  }


  handleDelete = (stdid) => {
    // console.log(stdid);
    axios.post('http://127.0.0.1:9898/delete/'+ stdid).then((res) => {
    }).catch(err => {
      console.log(err)
    });
    let {students} = this.state;
    students = students.filter((obj) => obj.id !== stdid);
    this.setState({students});

  }


  handleTrain = () => {
    this.setState({is_loading_train: !this.state.is_loading_train, is_train: !this.state.is_train});
    axios.post('http://127.0.0.1:9898/train').then((res) => {
      if (res.data.status == 404){
        this.setState({is_loading_train: !this.state.is_loading_train, is_train: !this.state.is_train});
        this.notification_func('Thông báo', res.data.data ? res.data.data : 'Train không thành công! Vui lòng kiểm tra lại ảnh.')
      } else{
        this.setState({is_loading_train: !this.state.is_loading_train, is_train: !this.state.is_train});
        this.notification_func('Thông báo', 'Train thành công!')
      }
    }).catch(err => {
      this.setState({is_loading_train: !this.state.is_loading_train, is_train: !this.state.is_train});
      this.notification_func('Thông báo', 'Train không thành công! Vui lòng kiểm tra lại ảnh.')
    });
  }

  handleCancel = e => {
    this.setState({
      visible: false,
      isEdit: false,
      editData: {}
    });
  };

  componentDidMount() {
    // let std = [];
    // if (this.state.get_information) {
    //   fetch('http://127.0.0.1:9898/result').then(res => {
    //     console.log(res)
    //     return res.json();
    //   }).then(data => {
    //     console.log(data);
    //     this.setState({students: std})
    //   });
    // }
    
    navigator.mediaDevices.getUserMedia({video: true, audio: false}).then((stream) => {
      // console.log(stream);
      if (this.video){
        this.video.srcObject = stream;
        this.video.play();
      }
    });

  }
  
  componentDidUpdate(prevProps, prevState){
    // console.log(prevState.dataResult, this.state.dataResult,this.state.is_detect);
    if(prevState.dataResult !== this.state.dataResult && this.state.is_detect){
      if(this.state.dataResult){
        this.autoCapture();
        this.post_image_result();
        this.setState({dataResult: false});
      }
    }
  }

  autoCapture = () => {
    if (this.video && this.canvas) {
      var context = this.canvas.getContext('2d');
      context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
      var data = this.canvas.toDataURL('image/jpg');
      this.previewImage.src = data;
      this.setState({is_capture:!this.state.is_capture, image_edit: ""});
    }

  }
  post_image_result = () => {
    var date = new Date()
    var time = date.getTime()
    let {students} = this.state;
    this.setState({is_loading:true});
    fetch('http://127.0.0.1:9898/result', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        image: this.previewImage.src,
        name_image: 'test' + time.toString() + '.png',
        name_folder: 'test',
        type: 'test',
      })
    }).then(result => 
      result.json()
    ).then(data => {
      if(Array.isArray(data) && data.length){
        data.map((stu) => {
          let exist = students.find((s) => s.masv === stu.masv);
          if(!exist){
            students.push(stu);
            this.notification_func('Thông báo', 'Nhận diện sinh viên ' + stu.name + ' thành công!')
          }
        });
      }

      this.setState({dataResult: true, students, is_loading:false});
    }).catch(e => {
      this.setState({dataResult: true, students, is_loading:false});
      this.notification_func('Thông báo', 'Nhận diện không thành công!')
    });
  }

  post_data_add = () => {
    var date = new Date()
    var time = date.getTime()
    fetch('http://127.0.0.1:9898/image', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        image: this.previewImage.src,
        name_image: 'test' + time.toString() + '.png',
        name_folder: 'test',
        type: 'train',
      })
    }).then(result => {
      result.json();
    }).then(data => {
    });
  }


  RenderTableData = () => {
    const {students} = this.state;
    return (
      <div className="student_info">
        <h3>THÔNG TIN HỌC SINH</h3>
        <div className="student_info_table">
          <div className="student_info_table_scroll">
            <table>
              <thead>
                <tr>
                  <th>MASV</th>
                  <th>Tên</th>
                  <th>Tuổi</th>
                  <th>Lớp</th>
                  <th>Môn học</th>
                  <th>Hình ảnh gốc</th>
                  <th>Hình ảnh nhận dạng</th>
                  <th>Thời gian</th>
                </tr>
              </thead>
              <tbody>
                {students.map((student, index) => {
                  console.log(student);
                  const {masv, name, age, className, subject, image, image_new,created_at} = student;
                  return (
                    <tr key={index}>
                      <td>{masv}</td>
                      <td>{name}</td>
                      <td>{age}</td>
                      <td>{className}</td>
                      <td>{subject}</td>
                      <td>{<img src={image} style={{width:300, height: 200}}></img>}</td>
                      <td>{<img src={image_new} style={{width:300, height: 200}}></img>}</td>
                      <td>{created_at}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
        <div className="student_info_button">
          <button onClick={this.handleView} className="btn">DANH SÁCH</button>
              <button onClick={this.handleDetect} className="btn">{this.state.is_detect ? "HỦY" : "NHẬN DIỆN"}</button>
          <button onClick={this.handleViewReport} className="btn">THỐNG KÊ</button>
        </div>
      </div>
    )
  }
  
  //Fuction handling

  RenderActionEditAdd = (props) => { 
    const {visible, isEdit, editData} = props;
    return (
      <div>
        <Modal
          title={isEdit ? 'Sửa học sinh' : "Thêm học sinh"}
          visible={visible}
          onCancel={this.handleCancel}
          footer = {[]}
        >
          <Form
          {...this.layout}
          fields={this.state.fields}
          name="basic"
          onFinish={this.onFinish}
         >
          <Form.Item
            label="Tên học sinh:"
            name="name"
            rules={[{ required: true, message: 'Tên học sinh không được để trống!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Tuổi:"
            name="age"
            rules={[{ type: 'number', min: 0, max: 99 }]}
          >
           <InputNumber />
          </Form.Item>

          <Form.Item
            label="Lớp:"
            name="className"
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Địa chỉ:"
            name="address"
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Số điện thoại:"
            name="phone"
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Môn học:"
            name="subject"
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Ảnh"
            name="image"
          >
            {this.state.image_edit ? <img src={this.state.image_edit} style={{width:300, height: 200}}/> : null}
            <canvas style={{display: this.state.is_capture && !this.state.image_edit ? 'block' : 'none', width: 300, height:200}} ref={(el) => this.canvas = el}></canvas>
            <video style={{display: this.state.is_capture ? 'none' : 'block', width: 300, height:200}} ref={(el) => this.video = el}></video>
            <Button style ={{marginTop: 5}} onClick={this.autoCapture} type="primary">
              { this.state.is_capture ? 'Chụp lại' : 'Chụp ảnh' }
            </Button>
          </Form.Item>
          <Form.Item {...this.tailLayout}>
            <Button type="primary" htmlType="submit">
              {this.state.isEdit ? 'Lưu lại' : 'Tạo học sinh'}
            </Button>
          </Form.Item>
        </Form>
        </Modal>
    </div>
    )

  }
  
  handleExit = () => {
    this.setState({is_report:false, status_view:false});
  }

  handleView = () => {
    console.log(this.state.status_view);
    if (this.state.status_view) {
      navigator.mediaDevices.getUserMedia({video: true, audio: false}).then((stream) => {
        if (this.video){
          this.video.srcObject = stream;
          this.video.play();
        }
      });
      this.setState({students:[]});
    }
    if (!this.state.status_view){
      let std = [];
      fetch('http://127.0.0.1:9898/getAll').then(res => {
        console.log(res)
        return res.json();
        }).then(data => {
          std = data.map(obj => {
            return{
              ...obj,
              image: obj.image + `?t=${Date.now()}`
            }
          })
          this.setState({students: std})
        });
    }
    this.setState({status_view: !this.state.status_view});

  }

  handleReport = () => {
    let [d1, d2] = this.state.dateRanger;
    fetch('http://127.0.0.1:9898/report', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: d1 && d1.format('YYYY-MM-DD HH:mm:ss'),
        to: d2 && d2.format('YYYY-MM-DD HH:mm:ss'), 
      })
    }).then(result => 
      result.json()
    ).then(data => {
      console.log(data);
      this.setState({student_report: data})
    }).catch(
      this.notification_func('')

    );
  }

  RederReport = () => {
    let students = this.state.student_report;
    return (
      <div className="wrapper_body_left">
        <div className="student_info">
            <h3>THỐNG KÊ</h3>
            <div className="date">
              <DatePicker.RangePicker format="YYYY-MM-DD" style={{width:400}} onChange={(e) => this.setState({dateRanger: e})}></DatePicker.RangePicker>
              <Button type="primary" onClick={this.handleReport} style={{marginLeft:5}}>THỐNG KÊ</Button>
            </div>
            <div className="student_info_table">
              <div className="student_info_table_scroll">
                <table>
                  <thead>
                    <tr>
                      <th>MASV</th>
                      <th>Tên</th>
                      <th>Tuổi</th>
                      <th>Lớp</th>
                      <th>Môn học</th>
                      <th>Thời gian</th>
                    </tr>
                  </thead>
                  <tbody>
                    {students.map((student, index) => {
                      const {masv, name, age, className, subject, created_at} = student;
                      return (
                        <tr key={index}>
                          <td>{masv}</td>
                          <td>{name}</td>
                          <td>{age}</td>
                          <td>{className}</td>
                          <td>{subject}</td>
                          <td>{created_at}</td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
            <div className="student_info_button">
              <button onClick={this.handleExit} className="btn">THOÁT</button>
            </div>
          </div>
      </div>
          
    );
  }

  RenderViewData = () => {
    const {students} = this.state;
    return (
      <div className="wrapper_body_left">
      <div className="student_info">
        <h3>DANH SÁCH HỌC SINH</h3>
        <div className="student_info_table">
          <div className="student_info_table_scroll">
            <table>
              <thead>
                <tr>
                  <th>MaSV</th>
                  <th>Tên</th>
                  <th>Tuổi</th>
                  <th>Lớp</th>
                  <th>Số điện thoại</th>
                  <th>Môn học</th>
                  <th>Hình ảnh</th>
                  <th width="100"></th>
                </tr>
              </thead>
              <tbody>
                {students.map((student, index) => {
                  const {masv, name, age, className, phone,subject, image} = student;
                  return (
                    <tr key={index}>
                      <td>{masv}</td>
                      <td>{name}</td>
                      <td>{age}</td>
                      <td>{className}</td>
                      <td>{phone}</td>
                      <td>{subject}</td>
                      <td><img src= {image}/></td>
                      <td>
                        <Button title="Sửa" onClick={() => this.showEdit(student)} style={{backgroundColor: 'blue', color: '#fff'}} icon={<EditOutlined />}></Button>
                        <Popconfirm title="Xác nhận xóa？" style={{minWidth: 200}} icon={<QuestionCircleOutlined style={{ color: 'red' }} />} onConfirm={() => this.handleDelete(student.id)}>
                          <Button title="Xóa" style={{marginLeft: 5, backgroundColor: '#f00', color: '#fff'}} icon={<DeleteOutlined />}></Button>
                        </Popconfirm>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
        <div className="student_info_button">
          <button onClick={this.showAdd} className="btn">THÊM</button>
          <div className="wrapper_body">
            {this.state.is_loading_train ? 
            <div className="loading">
              <div className="over"></div>
              <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />
              <span style={{color: '#fff'}}>Train...</span>
            </div> : ''}
          </div>
            <button onClick={this.handleTrain} className="btn">{this.state.is_train ? 'TRAIN DATA' : 'HỦY'}</button>
          <button onClick={this.handleView} className="btn">THOÁT</button>
        </div>
        </div>
        {this.state.visible ? <this.RenderActionEditAdd visible={this.state.visible} isEdit={this.state.isEdit} editData={this.state.editData}/> : null}
      </div>
    )
  }

  onLogin = (username, password) => {
    if(username == "admin" && password == "123456"){
      this.setState({check_login: true});
    }else{
      this.notification_func('Đăng nhập thất bại', 'Tài khoản hoặc mật khẩu không chính xác!');
    }
  }

  render(){
    let check_login = this.state.check_login;
    if (!check_login){
      return <Login onLogin={this.onLogin}/>;
   }
    return (
      <div className="wrapper">
        <div className="wrapper_header">
          <div className="wrapper_header_icon">
            <img src="/icon_school.jpg" alt=""/>
          </div>
          <div className="wrapper_header_text">
            <h3>HỆ THỐNG NHẬN DIỆN KHUÔN MẶT</h3>
          </div>
          <div className="wrapper_header_preview">
            <img ref={(el) => this.previewImage = el} src="" alt="Preview Image"/>
            
          </div>
        </div>
        <div className="wrapper_body">
          {this.state.is_loading ? 
          <div className="loading" style={{top: 145, right:5, bottom:'unset', left: 'unset'}}>
            <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />
            <span style={{color: '#fff'}}>Loading</span>
          </div> : ''}

          {
            this.state.status_view  ? <this.RenderViewData/> : (this.state.is_report ? <this.RederReport/> : <><div className="wrapper_body_left">
            <this.RenderTableData/>
          </div>
          <div className="wrapper_body_right">
            <div className="video">
              <video ref={(el) => this.video = el}></video>
              <canvas ref={(el) => this.canvas = el}></canvas>
            </div>
          </div></>
            )}

          
          
        </div>
      </div>
    );
  }
}

export default App;
