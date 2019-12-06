import React, {useEffect,useState} from 'react'
import axios from 'axios'
import Form from './Form'


const Main = () => {
    const [blocks, setBlocks] = useState([]);

    useEffect(() => {
        axios
        .get('http://localhost:5000/chain')
        .then(res => {
            console.log(res)
            setBlocks(res.data.chain)
        })
        .catch(err =>
            console.error(err))

    },[])


    const blockMap = blocks.map(block => {
        return block.transactions
    })

    const new_filter = blockMap.filter(blah => 
        blah.length > 0
    )
    const new_arr = []
    const combine = new_arr.concat(...new_filter)

    console.log(combine)

    const filteredRecipients = (id) => {
       return combine.filter(recip => recip.recipient == id)  
    }


    // console.log(filteredRecipients('tyler'))

    const filteredSenders = (id) => {
        return combine.filter(sender => sender.sender == id)
    }

    // console.log(filteredSenders('tyler'))
    
    return(
        <div>
        <Form filteredRecipients={filteredRecipients} filteredSenders={filteredSenders}/>
        </div>
    )
    
}

export default Main