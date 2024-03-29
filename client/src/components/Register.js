import { useEffect,useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Button, Checkbox, Form, Input,Modal,message } from 'antd';


import axios from "axios";

function Register()
{
     useEffect(()=>{
          if ("geolocation" in navigator) {
            // Get the user's current location
            navigator.geolocation.getCurrentPosition(
              function (position) {
                // The user's latitude and longitude are in position.coords.latitude and position.coords.longitude
                const Clatitude = position.coords.latitude;
                const Clongitude = position.coords.longitude;
               setLatitude(Clatitude)
               setLongitude(Clongitude)

                console.log(`Latitude: ${Clatitude}, Longitude: ${Clongitude}`);
              },
              function (error) {
                // Handle errors, if any
                switch (error.code) {
                  case error.PERMISSION_DENIED:
                    console.error("User denied the request for geolocation.");
                    break;
                  case error.POSITION_UNAVAILABLE:
                    console.error("Location information is unavailable.");
                    break;
                  case error.TIMEOUT:
                    console.error(
                      "The request to get user location timed out."
                    );
                    break;
                  case error.UNKNOWN_ERROR:
                    console.error("An unknown error occurred.");
                    break;
                }
              }
            );
          } else {
            console.error("Geolocation is not available in this browser.");
          }

     },[])
     const navigate = useNavigate();

     const [isModalOpen, setIsModalOpen] = useState(true);


    const [username,setUsername]=useState("")
    const [email,setEmail]=useState("")
    const [password,setPassword]=useState("")
    const [confirm_password,setConfirm_password]=useState("")
    const [dateOfBirth,setDateOfBirth]=useState("")
    const [longitude,setLongitude]=useState("")
    const [latitude,setLatitude]=useState("")

    const [usernameError,setUsernameError]=useState("")
    const [emailError,setEmailError]=useState("")
    const [passwordError,setPasswordError]=useState("")
    const [confirm_passwordError,setConfirm_passwordError]=useState("")
    const [dateOfBirthError,setDateOfBirthError]=useState("")
    const [longitudeError,setLongitudeError]=useState("")
    const [latitudeError,setLatitudeError]=useState("")

    const cleanErrors=()=>{
     setUsernameError("")
     setEmailError("")
     setPasswordError("")
     setConfirm_passwordError("")
     setDateOfBirthError("")
     setLongitudeError("")
     setLatitudeError("")
     }
     const handleCancel = () => {
    setIsModalOpen(false);
    window.location="/home"
  };

    const handleSubmit=(e)=>{
     
     e.preventDefault();
     const registrationBody = {username,email,password,confirm_password,dateOfBirth,longitude,latitude}
  
     console.log(registrationBody)
     axios.post("http://127.0.0.1:5000/auth/register",registrationBody)
     .then(response=>{
          if (response.status==200)
          {  cleanErrors()
             console.log(response.data,200)
             navigate('/preferences', { state: response.data });
          }
          if(response.status==206)
          {
               console.log(response.data,206)   
               if(response.data["errors"]["username"])
                    setUsernameError(response.data["errors"]["username"])
               else 
                    setUsernameError("")
               if(response.data["errors"]["password"])
                    setPasswordError(response.data["errors"]["password"])
               else
                    setPasswordError("")
                if (response.data["errors"]["confirm_password"])
                  setConfirm_passwordError(response.data["errors"]["confirm_password"]);
                else setConfirm_passwordError("");
               if (response.data["errors"]["email"])
                 setEmailError(response.data["errors"]["email"]);
               else setEmailError("");
               if(response.data["errors"]["dateofbirth"])
                    setDateOfBirthError(response.data["errors"]["dateofbirth"])
               else
                    setDateOfBirthError("")
          }
         }
         )
     .catch(error=>{console.error('Error:', error);
     });
}
    const onLogIn =()=>{
     setIsModalOpen(false)
     window.location="/login"


}
   return (
     <Modal
       title="Sign up now!"
       open={isModalOpen}
       onOk={handleSubmit}
       onCancel={handleCancel}
     >
       <article className="article-register">
         <section className="wrapper">
           <div className="form-register"></div>
           <header>Signup</header>
           <form>
             <div className="form-control">
               <input
                 type="text"
                 className="input-register"
                 placeholder="Username"
                 id="username"
                 name="username"
                 value={username}
                 required
                 
                 onChange={(e) => setUsername(e.target.value)}
               />
               {usernameError && <div className="error">{usernameError}</div>}
             </div>
             <div className="form-control">
               <input
                 type="email"
                 className="input-register"
                 placeholder="Email"
                 id="email"
                 name="email"
                 value={email}
                 required
                 onChange={(e) => setEmail(e.target.value)}
               />
               {emailError && <div className="error">{emailError}</div>}
             </div>

             <div className="form-control">
               <input
                 type="password"
                 className="input-register"
                 placeholder="Password"
                 id="password"
                 name="password"
                 value={password}
                 required
                 onChange={(e) => setPassword(e.target.value)}
               />
               {passwordError && <div className="error">{passwordError}</div>}
             </div>
             <div className="form-control">
               <input
                 type="password"
                 className="input-register"
                 placeholder="Confirm password"
                 id="confirm_password"
                 name="confirm_password"
                 value={confirm_password}
                 required
                 onChange={(e) => setConfirm_password(e.target.value)}
               />
               {confirm_passwordError && (
                 <div className="error">{confirm_passwordError}</div>
               )}
             </div>
             <div className="form-control">
               <input
                 type="date"
                 className="input-register"
                 placeholder="Date of birth"
                 id="dateOfBirth"
                 name="dateOfBirth"
                 value={dateOfBirth}
                 required
                 onChange={(e) => setDateOfBirth(e.target.value)}
               />
               {dateOfBirthError && (
                 <div className="error">{dateOfBirthError}</div>
               )}
             </div>
             <div className="form-control">
               {longitudeError && <div className="error">{longitudeError}</div>}
             </div>
             <div className="form-control">
               {latitudeError && <div className="error">{latitudeError}</div>}
             </div>
           </form>
           <Button type="link" htmlType="button" onClick={onLogIn}>
             Already have an account? Log in
           </Button>
         </section>
       </article>
     </Modal>
   );
}
export default Register
