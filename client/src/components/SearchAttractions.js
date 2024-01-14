import { useEffect, useState } from "react";
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Card,Space,Input,Button,Empty } from 'antd';
import { useNavigate } from 'react-router-dom';
import { getUserId } from "../utils";

 const { Meta } = Card;
  const {Search}=Input;
  const cardStyle = {
    width: 620,
  };
  const imgStyle = {
    display: 'block',
    width: 273,
    };
const SearchAttractions=()=>
{

 
  const location = useLocation();
  const navigate = useNavigate();

  const searchedText = location.state;


  const token=localStorage.getItem("token")
  const [defaultValue,setDefaultValue]=useState(searchedText)
    // const [hasToken,setHasToken]=useState(null)
  const [typeOfSearch,setTypeOfSearch]=useState("All")
  const [listOfAttractions,setListOfAttractions]=useState([])


    const handleOnSearch=(value, _e, info) => {
    // setDefaultValue("")
    console.log(value)
    console.log(searchedText)

    if(token===null)
        axios.get(`http://127.0.0.1:5000/user/searchEngineNotLoggedIn/${value}`)
        .then(responce=>{
            if(responce.status===200)
            {
              setListOfAttractions(responce.data)
              console.log(responce.data)
              console.log(listOfAttractions)
            }
        })
         .catch(error=>{console.error('Error:', error);
     });
    else{
          const id=getUserId()
          console.log(typeOfSearch)
         axios.get(`http://127.0.0.1:5000/user/searchEngine${typeOfSearch}/${id}/${value}`,{ headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } })
        .then(responce=>{
            if(responce.status===200)
            {
              setListOfAttractions(responce.data)
              console.log(responce.data)
              console.log(listOfAttractions)
            }
        })
         .catch(error=>{console.error('Error:', error);
     });
    }
    console.log(listOfAttractions)
    

      };
      const handleOnClick=(id)=>{
        console.log(id)
        navigate('/attraction', { state: id });
    }

    // useEffect(()=>{
    //     const t=localStorage.getItem("token")
    //     if(t!=null)
    //         setHasToken(t)
    // },[])
        useEffect(()=>{
       handleOnSearch(searchedText)
      //  TODO: Pitaj nekog 
    },[])
    // TODO: TREBA LI OVAKO SAMO JEDNOM? I STA AKO ISTEKNE TOKEN U MEDJUVREMENU IMAM TO U APP,ALI CE LI RADI OVDE
      


    return (
      <>
        <Search
          style={{ marginTop: "20px", marginBottom: "20px" }}
          placeholder={"Search " + typeOfSearch}
          onSearch={handleOnSearch}
          enterButton
        />
        <section>
          {token ? (
            <>
              {typeOfSearch != "All" && (
                <Button
                  type="link"
                  htmlType="button"
                  onClick={() => setTypeOfSearch("All")}
                >
                  #all
                </Button>
              )}
              {typeOfSearch != "City" && (
                <Button
                  type="link"
                  htmlType="button"
                  onClick={() => setTypeOfSearch("City")}
                >
                  #city
                </Button>
              )}
              {typeOfSearch != "AttractionName" && (
                <Button
                  type="link"
                  htmlType="button"
                  onClick={() => setTypeOfSearch("AttractionName")}
                >
                  #attractionName
                </Button>
              )}
              {typeOfSearch != "Hashtag" && (
                <Button
                  type="link"
                  htmlType="button"
                  onClick={() => setTypeOfSearch("Hashtag")}
                >
                  #hashtags
                </Button>
              )}
              {typeOfSearch != "Activity" && (
                <Button
                  type="link"
                  htmlType="button"
                  onClick={() => setTypeOfSearch("Activity")}
                >
                  #activity
                </Button>
              )}
            </>
          ) : (
            <></>
          )}
        </section>
        <Space size={[8, 16]} wrap>
          {listOfAttractions.length != 0 ? (
            listOfAttractions.map((item) => (
              <Card
                hoverable
                value={item["id"]}
                id={item["id"]}
                style={{
                  width: 240,
                }}
                onClick={() => handleOnClick(item["id"])}
                cover={
                  <img
                    alt="example"
                    src={item["image"]}
                    style={{
                      display: "block",
                      width: "100%",
                      height: "30vh",
                    }}
                  />
                }
              >
                <Meta title={item["name"]} />
              </Card>
            ))
          ) : (
            <>
              {" "}
              <Empty style={{ marginTop: "20px" }} />
            </>
          )}
        </Space>
      </>
    );
}
export default SearchAttractions