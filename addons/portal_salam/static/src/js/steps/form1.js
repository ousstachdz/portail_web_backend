class Form1 extends Component {
  static props = ['state', 'data']

  setup() {
    this.state = useState({
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
      },
    })
    this.handleChange = this.handleChange.bind(this)
    this.handleChangeArabicName = this.handleChangeArabicName.bind(this)
  }

  handleChange(event) {
    console.log('arabicLetters')
    const { state } = this.props
    const { name, value } = event.target
    if (name != 'nom_arabe') {
      state.formData[name] = value
    }
  }
  handleChangeArabicName(event) {
    event.preventDefault()

    const removeNonArabicLetters = (value) => {
      return value.replace(/[^\u0600-\u06FF\s]/g, '')
    }

    const cleanValue = removeNonArabicLetters(event.target.value)
    const { state } = this.props

    console.log('cleanValue', cleanValue)

    state.formData.nom_arabe = cleanValue

    event.target.value = cleanValue
  }

  static template = xml`
  <div class="d-flex flex-column align-items-center">
  <div class="col-md-12">
    <div class="bg-light p-3 rounded shadow-sm mb-4">
      <h5>معلومات أساسية</h5>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="name">اسم المتعامل <span class="field-require">*</span></label>
            <input
              type="text"
              name="name"
              t-att-value="state.formData.name"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل اسم المتعامل"
            />
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="nom_arabe">الاسم بالاحرف العربية <span class="field-require">*</span></label>
            <input
              type="text"
              name="nom_arabe"
              t-att-value="state.formData.nom_arabe"
              class="form-control"
              required="required"
              t-on-keyup="handleChangeArabicName"
              placeholder="أدخل الاسم بالأحرف العربية"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="bg-light p-3 rounded shadow-sm mb-4">
      <h5>معلومات الاتصال</h5>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="phone">رقم الهاتف <span class="field-require">*</span></label>
            <input
              type="text"
              name="phone"
              t-att-value="state.formData.phone"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل رقم الهاتف"
            />
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="email_from">البريد الإلكتروني <span class="field-require">*</span></label>
           <span dir="ltr" class="text-right">
            <input
              type="text"
              name="email_from"
              t-att-value="state.formData.email_from"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل البريد الإلكتروني"
            />
           </span>
            </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="siteweb">الموقع الإلكتروني <span class="field-require">*</span></label>
            <span dir="ltr" class="text-right">
            <input
              type="text"
              name="siteweb"
              t-att-value="state.formData.siteweb"
              class="form-control"
              placeholder="مثال: www.example.com"
              required="required"
              t-on-keyup="handleChange"
            />
           </span>

          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="adress_siege">عنوان المقر الاجتماعي <span class="field-require">*</span></label>
            <input
              type="text"
              name="adress_siege"
              t-att-value="state.formData.adress_siege"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل عنوان المقر الاجتماعي"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="bg-light p-3 rounded shadow-sm mb-4">
      <h5>تفاصيل التسجيل التجاري</h5>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="nif">رقم التعريف الضريبي (NIF) <span class="field-require">*</span></label>
            <input
              type="text"
              name="nif"
              t-att-value="state.formData.nif"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل رقم التعريف الضريبي"
            />
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="rc">رقم السجل التجاري (RC) <span class="field-require">*</span></label>
            <input
              type="text"
              name="rc"
              t-att-value="state.formData.rc"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل رقم السجل التجاري"
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="num_compte">رقم الحساب <span class="field-require">*</span></label>
            <input
              type="text"
              name="num_compte"
              t-att-value="state.formData.num_compte"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل رقم الحساب"
            />
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="date_ouverture_compte">تاريخ فتح الحساب <span class="field-require">*</span></label>
            <input
              type="date"
              name="date_ouverture_compte"
              t-att-value="state.formData.date_ouverture_compte"
              class="form-control"
              required="required"
              t-on-change="handleChange"
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="date_debut">تاريخ تأسيس الشركة <span class="field-require">*</span></label>
            <input
              type="date"
              name="date_debut"
              t-att-value="state.formData.date_debut"
              class="form-control"
              required="required"
              t-on-change="handleChange"
            />
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="date_debut_activite">تاريخ بداية النشاط <span class="field-require">*</span></label>
            <input
              type="date"
              name="date_debut_activite"
              t-att-value="state.formData.date_debut_activite"
              class="form-control"
              required="required"
              t-on-change="handleChange"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="bg-light p-3 rounded shadow-sm mb-4">
      <h5>معلومات النشاط</h5>
      <div class="row">

        <div class="col-md-6">
          <div class="form-group">
            <label for="forme_jur">الشكل القانوني <span class="field-require">*</span></label>
            <select
              name="forme_jur"
              id="forme_jur"
              class="form-control link-style"
              t-att-value="state.formData.forme_jur"
              t-on-change="handleChange"
            >
              <option value="" disabled="1" selected="1">
                اختر الشكل القانوني
              </option>
              <t
                t-foreach="props.data.forme_jurs"
                t-as="forme_jur"
                t-key="forme_jur.id"
              >
                <option t-att-value="forme_jur.id">
                  <t t-esc="forme_jur.name" t-att-value="forme_jur.id" />
                </option>
              </t>
            </select>
          </div>
        </div>

        <div class="col-md-6">
          <div class="form-group">
            <label for="activity_code">رمز النشاط حسب السجل التجاري <span class="field-require">*</span></label>
            <input
              type="text"
              name="activity_code"
              t-att-value="state.formData.activity_code"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل رمز النشاط"
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="activity_description">النشاط حسب السجل التجاري <span class="field-require">*</span></label>
            <input
              type="text"
              name="activity_description"
              t-att-value="state.formData.activity_description"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل وصف النشاط"
            />
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="activite_sec"
              >رمز النشاط الثانوي في السجل التجاري <span class="field-require">*</span></label>
            <input
              type="text"
              name="activite_sec"
              t-att-value="state.formData.activite_sec"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل رمز النشاط الثانوي"
            />
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="date_inscription">تاريخ القيد في السجل التجاري <span class="field-require">*</span></label>
            <input
              type="date"
              name="date_inscription"
              t-att-value="date_inscription"
              t-on-change="handleChange"
              class="form-control"
              required="required"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="bg-light p-3 rounded shadow-sm mb-4">
      <h5>المعلومات المالية</h5>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="chiffre_affaire">رأس المال <span class="field-require">*</span></label>
            <input
              type="number"
              name="chiffre_affaire"
              t-att-value="state.formData.chiffre_affaire"
              class="form-control"
              required="required"
              t-on-keyup="handleChange"
              placeholder="أدخل رأس المال"
            />
          </div>
        </div>
        <div class="col-md-6">
          <div class="form-group">
            <label for="chiffre_affaire_creation"
              >رأس المال عند الإنشاء<span class="field-require">*</span></label
            >
            <input
              type="number"
              name="chiffre_affaire_creation"
              t-att-value="state.formData.chiffre_affaire_creation"
              class="form-control"
              t-on-keyup="handleChange"
              placeholder="أدخل رقم الأعمال عند الإنشاء"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="bg-light p-3 rounded shadow-sm mb-4">
      <h5>معلومات الطلب</h5>
      <div class="row">
        <div class="col-md-6">
          <div class="form-group">
            <label for="demande">الطلب <span class="field-require">*</span></label>
            <select
              name="demande"
              id="demande"
              class="form-control link-style"
              t-att-value="state.formData.demande"
              t-on-change="handleChange"
            >
              <option value="" disabled="1" selected="1">اختر الطلب</option>
              <t
                t-foreach="props.data.demandes"
                t-as="demande"
                t-key="demande.id"
              >
                <option t-att-value="demande.id">
                  <t t-esc="demande.name" />
                </option>
              </t>
            </select>
          </div>
        </div>
        <div class="col-md-6"></div>
      </div>
      <div class="form-group">
        <label for="explanation">الغرض من الطلب <span class="field-require">*</span></label>
        <textarea
          id="explanation"
          name="explanation"
          class="form-control"
          rows="5"
          required="required"
          t-att-value="state.formData.explanation"
          t-on-keyup="handleChange"
          placeholder="أدخل الغرض من الطلب"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="description_company">تعريف الشركة <span class="field-require">*</span></label>
        <textarea
          id="description_company"
          name="description_company"
          class="form-control"
          rows="5"
          required="required"
          t-att-value="state.formData.description_company"
          t-on-keyup="handleChange"
          placeholder="أدخل تعريف الشركة"
        ></textarea>
      </div>
    </div>
  </div>
</div>

`
}
