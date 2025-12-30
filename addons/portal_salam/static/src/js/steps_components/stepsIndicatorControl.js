const { useEffect } = owl

class StepsIndicatorControl extends Component {
  static props = ['state']

  setup() {
    this.state = useState({
      isValid: false,
    })
    useEffect(
      () => {
        console.log('useEffect...')

        this.updateValidity()
      },
      () => [
        this.props.state.step,
        this.props.state.formData.name,
        this.props.state.formData.phone,
        this.props.state.formData.email_from,
        this.props.state.formData.siteweb,
        this.props.state.formData.adress_siege,
        this.props.state.formData.nif,
        this.props.state.formData.rc,
        this.props.state.formData.num_compte,
        this.props.state.formData.date_ouverture_compte,
        this.props.state.formData.date_debut,
        this.props.state.formData.nom_arabe,
        this.props.state.formData.date_debut_activite,
        this.props.state.formData.date_inscription,
        this.props.state.formData.activity_code,
        this.props.state.formData.activity_description,
        this.props.state.formData.activite_sec,
        this.props.state.formData.forme_jur,
        this.props.state.formData.chiffre_affaire,
        this.props.state.formData.chiffre_affaire_creation,
        this.props.state.formData.demande,
        this.props.state.formData.explanation,
        this.props.state.formData.description_company,
        this.props.state.partners.length,
        this.props.state.managers.length,
        this.props.state.tailles.length,
        this.props.state.situationTailles.length,
        this.props.state.suppliers.length,
        this.props.state.clients.length,
        this.props.state.companies.length,
        this.props.state.formData.document_1,
        this.props.state.formData.document_2,
        this.props.state.formData.document_3,
        this.props.state.formData.document_4,
        this.props.state.formData.document_5,
        this.props.state.formData.document_6,
        this.props.state.formData.document_7,
        this.props.state.formData.document_8,
        this.props.state.formData.document_9,
        this.props.state.formData.document_10,
        this.props.state.formData.document_11,
        this.props.state.formData.document_12,
        this.props.state.formData.document_13,
        this.props.state.formData.document_14,
        this.props.state.formData.document_15,
        this.props.state.formData.document_16,
        this.props.state.formData.password,
        this.props.state.formData.confirm_password,
      ]
    )
  }

  updateValidity() {
    this.state.isValid = false
    console.log('Updating validity...')
    if (this.stepOneValidation()) {
      this.state.isValid = true
    }
    if (this.stepTwoValidation()) {
      this.state.isValid = true
    }
    if (this.stepThreeValidation()) {
      this.state.isValid = true
    }
    if (this.stepFourValidation()) {
      this.state.isValid = true
    }
    // if (this.stepFiveValidation()) {
    //   this.state.isValid = true
    // }
  }

  previousStep() {
    const { state } = this.props
    if (state.step > 1) {
      state.step -= 1
    }
  }

  nextStep() {
    const { state } = this.props
    if (state.step < 4) {
      state.step += 1
    }
  }

  confirm() {
    const { state } = this.props
    // the url is like /portal-salam/{user_id}/{link_hash} or /{lang}/portal-salam/{user_id}/{link_hash}
    const url = window.location.href
    const urlParts = url.split('/')

    const user_id = urlParts[urlParts.length - 2]
    const link_hash = urlParts[urlParts.length - 1]

    console.log('user_id:', user_id)
    console.log('link_hash:', link_hash)

    const formData = {
      user_id: user_id,
      link_hash: link_hash,
      partners: state.partners,
      managers: state.managers,
      tailles: state.tailles,
      situationTailles: state.situationTailles,
      suppliers: state.suppliers,
      clients: state.clients,
      companies: state.companies,
      ...state.formData,
    }

    async function postData(data = {}) {
      const files = [
        'document_1',
        'document_2',
        'document_3',
        'document_4',
        'document_5',
        'document_6',
        'document_7',
        'document_8',
        'document_9',
        'document_10',
        'document_11',
        'document_12',
        'document_13',
        'document_14',
        'document_15',
        'document_16',
      ]

      const readFileAsBase64 = (file) => {
        return new Promise((resolve, reject) => {
          const reader = new FileReader()
          reader.onload = (e) => resolve(e.target.result)
          reader.onerror = (e) => reject(e)
          reader.readAsDataURL(file)
        })
      }

      const fileConversionPromises = files.map(async (fileKey) => {
        if (data[fileKey] && data[fileKey] instanceof File) {
          try {
            const base64String = await readFileAsBase64(data[fileKey])
            data[fileKey] = base64String
          } catch (error) {
            console.error(`Error reading file ${fileKey}:`, error)
            data[fileKey] = ''
          }
        }
      })

      await Promise.all(fileConversionPromises)

      const json_data = JSON.stringify(data)

      try {
        console.log(json_data)
        const response = await fetch('/opportunity/form_data/save', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': odoo.csrf_token,
          },
          body: json_data,
        })

        if (!response.ok) {
          console.error('Failed to send data:', response)
          return
        } else {
          state.step += 1
        }

        const result = await response.json()

        console.log('Server response:', result)
      } catch (error) {
        console.error('Error submitting data:', error)
      }
    }

    postData(formData)
  }

  stepOneValidation() {
    const { state } = this.props

    const fields = [
      'name',
      'phone',
      'email_from',
      'siteweb',
      'adress_siege',
      'nif',
      'rc',
      'num_compte',
      'date_ouverture_compte',
      'date_debut',
      'nom_arabe',
      'date_debut_activite',
      'date_inscription',
      'activity_code',
      'activity_description',
      'activite_sec',
      'forme_jur',
      'chiffre_affaire',
      'chiffre_affaire_creation',
      'demande',
      'explanation',
      'description_company',
    ]

    const emptyFields = fields.filter((field) => !state.formData[field] || state.formData[field] === '')

    if (emptyFields.length > 0) {
      console.log('The following fields are empty:', emptyFields)
    } else {
      console.log('All fields are filled.')
    }

    const isValid = state.step === 1 && emptyFields.length === 0

    console.log('Step 1 validation:', isValid)
    return isValid
  }

  stepTwoValidation() {
    const { state } = this.props

    return (
      state.step === 2
      // &&
      //   Array.isArray(state.partners) &&
      //   state.partners.length > 0 &&
      //   Array.isArray(state.managers) &&
      //   state.managers.length > 0 &&
      //   Array.isArray(state.tailles) &&
      //   state.tailles.length > 0
    )
  }

  stepThreeValidation() {
    const { state } = this.props
    return (
      state.step === 3
      //  &&
      // Array.isArray(state.situationTailles) &&
      // state.situationTailles.length > 0 &&
      // Array.isArray(state.suppliers) &&
      // state.suppliers.length > 0 &&
      // Array.isArray(state.clients) &&
      // state.clients.length > 0 &&
      // Array.isArray(state.companies) &&
      // state.companies.length > 0
    )
  }

  stepFourValidation() {
    const { state } = this.props
    const documents = [
      'document_1',
      'document_2',
      'document_7',
      'document_8',
      'document_12',
      'document_13',
      'document_15',
      'document_16',
    ]
    return state.step === 4
    // && documents.every((doc) => state.formData[doc] && state.formData[doc] !== '')
    // return true
  }

  stepFiveValidation() {
    const { state } = this.props
    state.formData.passwordSecurityLevel = 0
    const password = state.formData.password
    const confirmPassword = state.formData.confirm_password

    const hasUppercase = /[A-Z]/.test(password)
    const hasLowercase = /[a-z]/.test(password)
    const hasNumber = /\d/.test(password)
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password)

    if (hasUppercase) {
      state.formData.passwordSecurityLevel++
    }

    if (hasLowercase) {
      state.formData.passwordSecurityLevel++
    }
    if (hasNumber) {
      state.formData.passwordSecurityLevel++
    }

    if (hasSpecialChar) {
      state.formData.passwordSecurityLevel++
    }
    console.log('Password :', password)
    console.log('confirmPassword :', confirmPassword)
    console.log('passwordSecurityLevel :', state.formData.passwordSecurityLevel)

    if (password && password.length >= 8) {
      state.formData.passwordSecurityLevel++
    }

    if (password !== confirmPassword) {
      return false
    }

    if (state.formData.passwordSecurityLevel != 5) {
      return false
    }
    if (state.step === 5) {
      return true
    }
  }

  static template = xml`
      <div class="container">
                <t t-if="props.state.step &lt; 4">
                  <t t-if="state.isValid">
                    <button type="button" class="btn btn-primary green-btn" t-on-click="nextStep">
                    التالي
                    </button>
                  </t>
                </t>
                <t t-if="props.state.step &gt;= 2">
                  <t t-if="props.state.step &lt;= 4">
                    <button type="button" class="btn btn-secondary" t-on-click="previousStep">
                    السَّابِق
                    </button>
                  </t>
                </t>
                <t t-if="props.state.step === 4">
                <t t-if="state.isValid">
                <button type="button" class="btn btn-primary" t-on-click="confirm">
                    تأكيد
                </button>
                </t>
                </t>
            </div>
  `
}
