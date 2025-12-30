/// const { Component, useState, mount, xml } = owl
const { onMounted } = owl

class GlobalIndex extends Component {
  setup() {
    this.state = useState({
      step: 1,
      data: null,
      formData: {
        name: '',
        phone: '',
        email_from: '',
        siteweb: '',
        adress_siege: '',
        nif: '',
        rc: '',
        num_compte: '',
        date_ouverture_compte: '',
        date_debut: '',
        nom_arabe: '',
        date_debut_activite: '',
        date_inscription: '',
        activity_code: '',
        activity_description: '',
        activite_sec: '',
        forme_jur: '',
        chiffre_affaire: '',
        chiffre_affaire_creation: '',
        demande: '',
        explanation: '',
        description_company: '',
        document_1: null,
        document_2: null,
        document_3: null,
        document_4: null,
        document_5: null,
        document_6: null,
        document_7: null,
        document_8: null,
        document_9: null,
        document_10: null,
        document_11: null,
        document_12: null,
        document_13: null,
        document_14: null,
        document_15: null,
        document_16: null,
        password: '',
        confirm_password: '',
        passwordSecurityLevel: 0,
      },
      partners: [],
      managers: [],
      tailles: [],
      situationTailles: [],
      suppliers: [],
      clients: [],
      companies: [],
    })

    onMounted(async () => {
      try {
        const response = await fetch('/opportunity/form_data')
        if (response.ok) {
          const data = await response.json()
          this.state.data = data
          console.log('Data fetched:', data)
        } else {
          console.error('Failed to fetch data from API')
        }
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    })
  }

  static components = {
    StepsIndicator,
    StepsIndicatorControl,
    Form1,
    Form2,
    Form3,
    Form4,
    Form5,
    Form6,
  }

  static template = xml`
      <div>
        <StepsIndicator state="state"/>  
        <t t-if="state.data">
            <t t-if="state.step === 5">
            <Form6 state="state"/>
            </t>
            <t t-else="">
            <h3>املاء البيانات التالية</h3>
            <div class="alert alert-info" role="alert">
              الحقول التي تحتوي على "*" مطلوبة
            </div>
            </t>
          <div  t-attf-class="row {{ (state.step === 1) ? '' : 'd-none' }}">
            <Form1 state="state" data="state.data"/>  
          </div>
          <div  t-attf-class="row {{ (state.step === 2) ? '' : 'd-none' }}">
            <Form2 state="state"/>
          </div>
          <div  t-attf-class="row {{ (state.step === 3) ? '' : 'd-none' }}">
            <Form3 state="state"/>
          </div>
          <div  t-attf-class="row {{ (state.step === 4) ? '' : 'd-none' }}">
            <Form4 state="state"/>
          </div>
          </t>
          <t t-else="">
          <p>جارٍ تحميل البيانات...</p> 
          </t>
          <StepsIndicatorControl state="state"/>  
      </div>
    `
}

document.getElementById('form_portail') && mount(GlobalIndex, document.getElementById('form_portail'))

// <div  t-attf-class="row {{ (state.step === 5) ? '' : 'd-none' }}">
//   <Form5 state="state"/>
// </div>
