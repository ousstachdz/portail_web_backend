class Form2 extends Component {
  static props = ['state', 'data']
  setup() {
    this.state = useState({
      formData: {},
    })

    this.handleChange = this.handleChange.bind(this)
  }

  handleChange(event) {
    // const {s}
    const { state } = this.props
    const { name, value } = event.target
    state.formData[name] = value // Correctly update formData in the parent's state
  }

  static components = { Partners, ManagementTeam, FinancialRequestIndex }

  static template = xml`
      <div>
        <h5 for="apropos" style="font-size: 16px; font-weight:bold; color: #045444;">
          توزيع راس مال الشركة
        </h5>
        <div class="text-end mb-3">
          <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createAproposModal">
            اضف شريك
          </button>
        </div>

        <Partners state="props.state" />
      
        <h5 for="gestion" style="font-size: 16px; font-weight:bold; color: #045444;">
          فريق التسيير
        </h5>
        <div class="text-end mb-3">
          <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createGestionModal">
            اضف مسير
          </button>
        </div>
        <ManagementTeam state="props.state" />

        <h5 for="tailles" style="font-size: 16px; font-weight:bold; color: #045444;">
          حجم و هيكل التمويلات المطلوبة
        </h5>
        <div class="text-end mb-3">
          <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createRequestModal">
            اضف طلب
          </button>
        </div>
        <FinancialRequestIndex state="props.state" />
      </div>
    `
}
