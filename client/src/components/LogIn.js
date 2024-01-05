import React,{ useState } from 'react';
import { Button, Checkbox, Form, Input,Modal,message } from 'antd';
import axios from "axios";


const LogIn = () => {

const [username,setUsername]=useState("")
const [password,setPassword]=useState("")
const [isError,setIsError]=useState("")


const [isModalOpen, setIsModalOpen] = useState(true);

const [messageApi, contextHolder] = message.useMessage();
const loggedIn = () => {
    messageApi.open({
      type: 'success',
      content: 'You are logged in!',
      duration: 3,
    });
    setTimeout(() => {
    window.location = "/home";
  }, 3000);

  };
// const onFinish = (values) => {
//   console.log('Success:', values);
// };

const handleOk = () => {
  axios.get(`http://127.0.0.1:5000/auth/login/${username}/${password}`)
  .then(responce=>{
    if(responce.status===200)
    {
      console.log(responce.data["token"])
      localStorage.setItem("token", responce.data["token"]);

      loggedIn()
      //setIsModalOpen(false);
      // kada dodam windows.locatioon nece da mi se vidi ova poruka za login
    }
    else if (responce.status===206)
    {
      setIsError(responce.data["message"])
    }
  })
  };
  const handleCancel = () => {
    setIsModalOpen(false);
    window.location="/home"
  };
  return(
  <Modal  title="Log In now!" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
    {contextHolder}
    {/* <section className='wrapper'> */}
  <Form
    name="basic"
    className='wrapper'
    labelCol={{
      span: 8,
    }}
    wrapperCol={{
      span: 16,
    }}
    style={{
      maxWidth: 600
    }}
    initialValues={{
      remember: true,
    }}
    // onFinish={handleOk}
    // onFinishFailed={onFinishFailed}
    autoComplete="off"
  >
    <h1 style={{marginLeft:"30vh",color:"white"
}}>Log in</h1>
    <Form.Item
      label="Username"
      name="username"
      value={username}
      onChange={(e)=>setUsername(e.target.value)}

      rules={[
        {
          required: true,
          message: 'Please input your username!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Password"
      name="password"
      value={password}
      onChange={(e)=>setPassword(e.target.value)}
      rules={[
        {
          required: true,
          message: 'Please input your password!',
        },
      ]}
    >
      <Input.Password />
    </Form.Item>

    <Form.Item
      name="remember"
      valuePropName="checked"
      wrapperCol={{
        offset: 8,
        span: 16,
      }}
    >
      {isError && <div className="error">{isError}</div>}

      <Checkbox>Remember me</Checkbox>
    </Form.Item>

    <Form.Item
      wrapperCol={{
        offset: 8,
        span: 16,
      }}
    >
      {/* <Button type="primary" htmlType="submit" onClick={handleOk}>
        Submit
      </Button> */}
    </Form.Item>
  </Form>
  {/* </section> */}
  </Modal>
    
);
    }
export default LogIn;