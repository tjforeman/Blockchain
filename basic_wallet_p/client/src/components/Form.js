import React, {useEffect,useState} from 'react'
import Wallet from './Wallet'

const Form = (props) => {
    const[form, setId] = useState({
        id : '',
    })
    const [sent, setSent] = useState([]);
    const [recieved, setRecieved] = useState([]);

    const handleChange = name => event => {
        setId({ ...form, [name]: event.target.value });

    };

    const onSubmit = e => {
        e.preventDefault()

        setRecieved(props.filteredRecipients(form.id))
        setSent(props.filteredSenders(form.id))
    }

    console.log(sent)
    console.log(recieved)


    return(
        <div>
            <form onSubmit={onSubmit}> 
            <input value={form.id} placeholder ={'enter your id'} onChange={handleChange('id')} />
            <button>Submit</button>
            </form >
            <div>
                <Wallet sent={sent} recieved={recieved} />
            </div>


        </div>
    )

}

export default Form