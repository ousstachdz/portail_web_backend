// Define ClientsTable Component
class ClientsTable extends Component {
  static props = ['state']

  setup() {
    this.deleteClients = this.deleteClients.bind(this)
  }

  deleteClients(id, e) {
    e.preventDefault()
    console.log('Delete client with ID:', id)
    const state = this.props.state
    if (state) {
      state.clients = state.clients.filter((client) => client.id !== id)
    } else {
      console.error('State is not accessible in ClientsTable')
    }
  }

  static template = xml`
     <div class="tableWrapper">
      <table  class="table table-striped table-responsive">
        <thead class="fw-bold">
          <tr>
          <th>الاسم</th>
          <th>الجنسية</th>
          <th>طريقة السداد</th>
          <th>حذف</th>
        </tr>
      </thead>
      <tbody id="client">
        <t t-foreach="props.state.clients" t-as="client" t-key="client.id">
          <tr>
            <td><span><t t-esc="client.name"/></span></td>
            <td><span><t t-esc="client.countryName"/></span></td>
            <td>
              <ul>
                <t t-foreach="client.selectedPaymentsNames" t-as="selectedPayment" t-key="selectedPayment">
                  <li>-   <t t-esc="selectedPayment"/></li>
                </t>
              </ul>
            </td>
            <td>
              <button type="button" class="btn-delete" t-on-click="(e) => deleteClients(client.id, e)"><svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg></button>
            </td>
          </tr>
        </t>
      </tbody>
    </table>
    </div>
  `
}
// Define AddClients Component
class AddClients extends Component {
  static props = ['state']

  setup() {
    this.state = useState({
      name: '',
      country: '',
      countryName: '',
      selectedPayments: [],
      selectedPaymentsNames: [],
    })
  }

  handleSubmit(event) {
    event.preventDefault()

    const newClient = {
      id: Date.now(), // Generate a unique ID
      name: this.state.name,
      country: this.state.country,
      countryName: this.state.countryName,
      selectedPayments: this.state.selectedPayments, // Save selected payment IDs
      selectedPaymentsNames: this.state.selectedPaymentsNames, // Save selected payment names
    }

    const { state } = this.props
    if (state) {
      state.clients.push(newClient)
    } else {
      console.error('State is not accessible in AddClients')
    }

    // Reset form fields
    this.state.name = ''
    this.state.country = ''
    this.state.countryName = ''
    this.state.selectedPayments = []
    this.state.selectedPaymentsNames = []

    // Uncheck all checkboxes after submission
    document.querySelectorAll('.form-check-input').forEach((checkbox) => {
      checkbox.checked = false
    })
  }

  handlePaymentChange(event) {
    const paymentId = event.target.getAttribute('data-payment-id')
    const paymentName = event.target.getAttribute('data-payment-name')
    const isChecked = event.target.checked

    if (isChecked) {
      this.state.selectedPayments.push(paymentId) // Add payment ID
      this.state.selectedPaymentsNames.push(paymentName) // Add payment name
    } else {
      const idIndex = this.state.selectedPayments.indexOf(paymentId)
      if (idIndex !== -1) {
        this.state.selectedPayments.splice(idIndex, 1) // Remove payment ID
      }

      const nameIndex = this.state.selectedPaymentsNames.indexOf(paymentName)
      if (nameIndex !== -1) {
        this.state.selectedPaymentsNames.splice(nameIndex, 1) // Remove payment name
      }
    }
  }

  handleCountryChange(event) {
    const countryId = event.target.value
    const countryName = event.target.options[event.target.selectedIndex].text

    this.state.country = countryId
    this.state.countryName = countryName
  }

  static template = xml`
    <div class="modal fade" id="createClientModal" tabindex="-1" aria-labelledby="createClientModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
                    <div class="modal-header d-flex justify-content-between align-items-center">

                    <h5 class="modal-title" id="createClientModalLabel">اضف عميل</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form t-on-submit="handleSubmit" style="padding: 10px">
          <div class="modal-body">
              <div class="mb-3">
                <label for="name">السيد(ة)</label>
                <input type="text" t-model="state.name" class="form-control form-control-sm" id="name" name="name" required="required"/>
              </div>
              <div class="mb-3">
                <label for="country">الجنسية</label>
                <select t-model="state.country" name="country" id="country" class="form-control link-style" t-on-change="handleCountryChange">
                  <option value="" disabled="1" selected="1" >اختر الجنسية</option> 
                <t t-foreach="props.state.data.nationalites" t-as="country" t-key='country.id'>
                    <option t-att-value="country.id">
                      <t t-esc="country.name"/>
                    </option>
                  </t>
                </select>
              </div>
              <div class="mb-3">
                <label for="type_payment">طريقة السداد</label>
                <t t-foreach="props.state.data.type_payment_ids" t-as="type_payment" t-key="type_payment.id">
                  <div class="form-check">
                    <input type="checkbox" class="form-check-input" 
                          t-att-id="'type_payment_' + type_payment.id" 
                          t-att-name="'type_payment_' + type_payment.id"
                          t-att-value="type_payment.id"
                          t-att-data-payment-id="type_payment.id"
                          t-att-data-payment-name="type_payment.name"
                          t-on-change="handlePaymentChange"/>
                    <label class="form-check-label" t-att-for="'type_payment_' + type_payment.id">
                      <t t-esc="type_payment.name"/>
                    </label>
                  </div>
                </t>
              </div>
              </div>
              <div class="modal-footer">
              <button type="submit" class="btn btn-secondary">اضف</button>
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              </div>
              </form>
        </div>
      </div>
    </div>
  `
}

// Define ClientsIndex Component
class ClientsIndex extends Component {
  static props = ['state']

  static components = {
    ClientsTable,
    AddClients,
  }

  static template = xml`
    <div>
      <AddClients state="props.state"/>
      <ClientsTable state="props.state"/>
    </div>
  `
}
