// Define SuppliersTable Component
class SuppliersTable extends Component {
  static props = ['state']

  setup() {
    this.deleteSuppliers = this.deleteSuppliers.bind(this)
  }

  deleteSuppliers(id, e) {
    e.preventDefault()
    console.log('Delete supplier with ID:', id)
    const state = this.props.state
    if (state) {
      state.suppliers = state.suppliers.filter((supplier) => supplier.id !== id)
    } else {
      console.error('State is not accessible in SuppliersTable')
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
      <tbody id="supplier">
        <t t-foreach="props.state.suppliers" t-as="supplier" t-key="supplier.id">
          <tr>
            <td><span><t t-esc="supplier.name"/></span></td>
            <td><span><t t-esc="supplier.countryName"/></span></td>
            <td>
              <ul>
                <t t-foreach="supplier.selectedPaymentsNames" t-as="selectedPayment" t-key="selectedPayment">
                  <li>-   <t t-esc="selectedPayment"/></li>
                </t>
              </ul>
            </td>
            <td>
              <button type="button" class="btn btn-danger" t-on-click="(e) => deleteSuppliers(supplier.id, e)">حذف</button>
            </td>
          </tr>
        </t>
      </tbody>
    </table>
    </div>

  `
}
// Define AddSuppliers Component
class AddSuppliers extends Component {
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

    const newSupplier = {
      id: Date.now(), // Generate a unique ID
      name: this.state.name,
      country: this.state.country,
      countryName: this.state.countryName,
      selectedPayments: this.state.selectedPayments, // Save selected payment IDs
      selectedPaymentsNames: this.state.selectedPaymentsNames, // Save selected payment names
    }

    const { state } = this.props
    if (state) {
      state.suppliers.push(newSupplier)
    } else {
      console.error('State is not accessible in AddSuppliers')
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
    <div class="modal fade" id="createSupplierModal" tabindex="-1" aria-labelledby="createSupplierModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
                    <div class="modal-header d-flex justify-content-between align-items-center">

                    <h5 class="modal-title" id="createSupplierModalLabel">اضف مورد</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form t-on-submit="handleSubmit" style="padding: 10px">
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
              <button type="submit" class="btn btn-secondary">اضف</button>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  `
}

// Define SuppliersIndex Component
class SuppliersIndex extends Component {
  static props = ['state']

  static components = {
    SuppliersTable,
    AddSuppliers,
  }

  static template = xml`
    <div>
      <AddSuppliers state="props.state"/>
      <SuppliersTable state="props.state"/>
    </div>
  `
}
