import { useEffect,useState } from "react";
import axios from "axios";

function Register()
{
    const [username,setUsername]=useState("")
    const [email,setEmail]=useState("")
    const [password,setPassword]=useState("")
    const [confirm_password,setConfirm_password]=useState("")
    const [dateOfBirth,setDateOfBirth]=useState("")
    const [longitude,setLongitude]=useState("")
    const [latitude,setLatitude]=useState("")


    const handleSubmit=(e)=>{
     e.preventDefault();
     const registrationBody={username,email,password,confirm_password,dateOfBirth,longitude,latitude}
  
     console.log(registrationBody)
     axios.post("http://127.0.0.1:5000/auth/register",registrationBody)
     .then(response=>{
          if (response.status==200)
          {
               
          }
         }
         )
     .catch(error=>{console.error('Error:', error);
     });
}
   return(
    <>
    <article>
       <form onSubmit={handleSubmit}>
        <div className="form-control">
            <label htmlFor="username">Username:</label>
            <input type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e)=>setUsername(e.target.value)}
             />
        </div>
        <div className="form-control">
            <label htmlFor="email">Email:</label>
            <input type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
             />
        </div>

        <div className="form-control">
            <label htmlFor="password">Password:</label>
            <input type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
             />
        </div>
             <div className="form-control">
            <label htmlFor="confirm_password">Confirm Password:</label>
            <input type="password"
            id="confirm_password"
            name="confirm_password"
            value={confirm_password}
            onChange={(e)=>setConfirm_password(e.target.value)}
             />
        </div>
             <div className="form-control">
            <label htmlFor="dateOfBirth">Date of birth:</label>
            <input type="date"
            id="dateOfBirth"
            name="dateOfBirth"
            value={dateOfBirth}
            onChange={(e)=>setDateOfBirth(e.target.value)}
             />
        </div>
             <div className="form-control">
            <label htmlFor="longitude">Longitude:</label>
            <input type="number"
            id="longitude"
            name="longitude"
            value={longitude}
            onChange={(e)=>setLongitude(e.target.value)}
             />
        </div>
        <div className="form-control">
            <label htmlFor="latitude">Latitude:</label>
            <input type="number"
            id="latitude"
            name="latitude"
            value={latitude}
            onChange={(e)=>setLatitude(e.target.value)}
             />
        </div>
        <button type="submit">Next</button>

       </form>


    </article>
    </>

   );
}
export default Register
