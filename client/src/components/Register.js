// import { useEffect,useState } from "react";
// function Register()
// {
//    const [forma,setForma]=useState({})
//    useEffect(
//       ()=>{
//          fetch("/auth/register").then(res => res.json()).then(data => {
//          console.log("e usao i fetch")
//          console.log(data)
//          setForma(data)

//     });
//       }
//    );
//    console.log(" odradio rerender")
//    return (
//    <>
//        <div class="content-section">
//         <form method="POST" action="">
//             {{forma.hidden_tag()}}
//             <fieldset class ="form-group">
//                 <legend  class="border-bottom mb-4">Join Today </legend>
//                 <div class="form-group">
//                     {{ forma.username.label(class="form-control-label") }}

//                     {% if forma.username.errors %}
//                         {{ forma.username(class="form-control form-control-lg is-invalid") }}
//                         <div class="invalid-feedback">
//                             {% for error in forma.username.errors %}
//                                 <span>{{ error }}</span>
//                             {% endfor %}
//                         </div>
//                     {% else %}
//                         {{ form.username(class="form-control form-control-lg") }}
//                     {% endif %}
//                 </div>
//                 <div class="form-group">
//                     {{ form.email.label(class="form-control-label") }}
//                     {% if form.email.errors %}
//                         {{ form.email(class="form-control form-control-lg is-invalid") }}
//                         <div class="invalid-feedback">
//                             {% for error in form.email.errors %}
//                                 <span>{{ error }}</span>
//                             {% endfor %}
//                         </div>
//                     {% else %}
//                         {{ form.email(class="form-control form-control-lg") }}
//                     {% endif %}
//                 </div>
//                 <div class="form-group">
//                     {{ form.password.label(class="form-control-label") }}
//                     {% if form.password.errors %}
//                         {{ form.password(class="form-control form-control-lg is-invalid") }}
//                         <div class="invalid-feedback">
//                             {% for error in form.password.errors %}
//                                 <span>{{ error }}</span>
//                             {% endfor %}
//                         </div>
//                     {% else %}
//                         {{ form.password(class="form-control form-control-lg") }}
//                     {% endif %}
//                 </div>
//                 <div class="form-group">
//                     {{ form.confirm_password.label(class="form-control-label") }}
//                     {% if form.confirm_password.errors %}
//                         {{ form.confirm_password(class="form-control form-control-lg is-invalid") }}
//                         <div class="invalid-feedback">
//                             {% for error in form.confirm_password.errors %}
//                                 <span>{{ error }}</span>
//                             {% endfor %}
//                         </div>
//                     {% else %}
//                         {{ form.confirm_password(class="form-control form-control-lg") }}
//                     {% endif %}
//                 </div>
//                 <div class="form-group">
//                     {{ form.dateofbirth.label(class="form-control-label") }}
//                     {% if form.dateofbirth.errors %}
//                         {{ form.dateofbirth(class="form-control form-control-lg is-invalid") }}
//                         <div class="invalid-feedback">
//                             {% for error in form.dateofbirth.errors %}
//                                 <span>{{ error }}</span>
//                             {% endfor %}
//                         </div>
//                     {% else %}
//                         {{ form.dateofbirth(class="form-control form-control-lg") }}
//                     {% endif %}
//                 </div>
//                 <div class="form-group">
//                     {{ form.longitude.label(class="form-control-label") }}
//                     {% if form.longitude.errors %}
//                         {{ form.longitude(class="form-control form-control-lg is-invalid") }}
//                         <div class="invalid-feedback">
//                             {% for error in form.longitude.errors %}
//                                 <span>{{ error }}</span>
//                             {% endfor %}
//                         </div>
//                     {% else %}
//                         {{ form.longitude(class="form-control form-control-lg") }}
//                     {% endif %}
//                 </div>
//                 <div class="form-group">
//                     {{ form.latitude.label(class="form-control-label") }}
//                     {% if form.latitude.errors %}
//                         {{ form.latitude(class="form-control form-control-lg is-invalid") }}
//                         <div class="invalid-feedback">
//                             {% for error in form.latitude.errors %}
//                                 <span>{{ error }}</span>
//                             {% endfor %}
//                         </div>
//                     {% else %}
//                         {{ form.latitude(class="form-control form-control-lg") }}
//                     {% endif %}
//                 </div>
//             </fieldset>
//             <div class="form-group">
//                 {{ form.submit(class="btn btn-outline-info") }}
//             </div>
//         </form>
//     </div>
//     <div class="border-top pt-3">
//         <small class="text-muted">
//             Already Have An Account? <a class="ml-2" href="{{ url_for('auth.login') }}">Sign In</a>
//         </small>
//     </div>
//    </>
//    );
// }
// export default Register