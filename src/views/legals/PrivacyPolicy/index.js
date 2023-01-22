import React from 'react'
import { useNavigate } from 'react-router-dom'

const PrivacyPolicy = () => {

    const navigate = useNavigate()
    const TermsClick = () => {
        navigate(`/app/legals/terms-and-conditions`)
    }

    // Styling
    const boldText = {
        fontWeight: 'bold',
        marginLeft: '5px'
    }
    const divStyle = {
        display: 'flex',
    }
    
	return (
		<div>
            <h3>
                Privacy Policy
            </h3>
            <div>
                <p>
                    This privacy policy applies between you, the User of this Website, and R2SA
                    Leads Limited, the owner and provider of this Website. R2SA Leads Limited
                    takes the privacy of your information very seriously. This privacy policy
                    applies to our use of any and all Data collected by us or provided by you
                    in relation to your use of the Website.
                </p>
                <br />
                <div style={divStyle}>
                    <p>
                        This privacy policy should be read alongside, and in addition to, our Terms
                        and Conditions, which can be found at:  
                    </p>
                    <button  style={boldText} onClick={TermsClick}> Terms and Conditions.</button>
                </div>

                <br />
                <p>
                    <strong>Please read this privacy policy carefully</strong>
                    .
                </p>
                <br />
                <p>
                    <strong>Definitions and interpretation</strong>
                </p>
                <p>
                    1. In this privacy policy, the following definitions are used:
                </p>
                <br />
                <table border="1" cellspacing="0" cellpadding="0">
                    <tbody>
                        <tr>
                            <td valign="top">
                                <p>
                                    <strong>Data</strong>
                                </p>
                            </td>
                            <td valign="top">
                                <p>
                                    collectively all information that you submit to R2SA Leads
                                    Limited via the Website. This definition incorporates,
                                    where applicable, the definitions provided in the Data
                                    Protection Laws;
                                </p>
                            </td>
                        </tr>
                        <br />
                        <tr>
                            <td valign="top">
                                <p>
                                    <strong>Data Protection Laws</strong>
                                </p>
                            </td>
                            <td valign="top">
                                <p>
                                    any applicable law relating to the processing of personal
                                    Data, including but not limited to the GDPR, and any
                                    national implementing and supplementary laws, regulations
                                    and secondary legislation;
                                </p>
                            </td>
                        </tr>
                        <br />
                        <tr>
                            <td valign="top">
                                <p>
                                    <strong>GDPR</strong>
                                </p>
                            </td>
                            <td valign="top">
                                <p>
                                    the UK General Data Protection Regulation;
                                </p>
                            </td>
                        </tr>
                        <br />
                        <tr>
                            <td valign="top">
                                <p>
                                    <strong>
                                        R2SA Leads Limited, 
                                        <br/>
                                        we 
                                    </strong>
                                      or <strong> us</strong>
                                </p>
                            </td>
                            <td valign="top">
                                <p>
                                    R2SA Leads Limited, a company incorporated in England and
                                    Wales with registered number 14522856 whose registered
                                    office is at Flat 2, Montrose House, 44 Princes Gate,
                                    London, SW7 2QA;
                                </p>
                            </td>
                        </tr>
                        <br />
                        <tr>
                            <td valign="top">
                                <p>
                                    <strong>User </strong>
                                     or <strong> you </strong>
                                </p>
                            </td>
                            <td valign="top">
                                <p>
                                    any third party that accesses the Website and is not either
                                    (i) employed by R2SA Leads Limited and acting in the course
                                    of their employment or (ii) engaged as a consultant or
                                    otherwise providing services to R2SA Leads Limited and
                                    accessing the Website in connection with the provision of
                                    such services; and
                                </p>
                            </td>
                        </tr>
                        <br />
                        <tr>
                            <td valign="top">
                                <p>
                                    <strong>Website</strong>
                                </p>
                            </td>
                            <td valign="top">
                                <p>
                                    the website that you are currently using, www.r2sa.co.uk,
                                    and any sub-domains of this site unless expressly excluded
                                    by their own terms and conditions.
                                </p>
                            </td>
                        </tr>
                        <br />
                    </tbody>
                </table>
                <p>
                    2. In this privacy policy, unless the context requires a different
                    interpretation:
                </p>
                <p>
                    a. the singular includes the plural and vice versa;
                </p>
                <p>
                    b. references to sub-clauses, clauses, schedules or appendices are to
                    sub-clauses, clauses, schedules or appendices of this privacy policy;
                </p>
                <p>
                    c. a reference to a person includes firms, companies, government entities,
                    trusts and partnerships;
                </p>
                <p>
                    d. "including" is understood to mean "including without limitation";
                </p>
                <p>
                    e. reference to any statutory provision includes any modification or
                    amendment of it;
                </p>
                <p>
                    f. the headings and sub-headings do not form part of this privacy policy.
                </p>
                <br />
                <p>
                    <strong>Scope of this privacy policy</strong>
                </p>
                <p>
                    3. This privacy policy applies only to the actions of R2SA Leads Limited
                    and Users with respect to this Website. It does not extend to any websites
                    that can be accessed from this Website including, but not limited to, any
                    links we may provide to social media websites.
                </p>
                <p>
                    4. For purposes of the applicable Data Protection Laws, R2SA Leads Limited
                    is the "data controller". This means that R2SA Leads Limited determines the
                    purposes for which, and the manner in which, your Data is processed.
                </p>
                <br />
                <p>
                    <strong>Data collected</strong>
                </p>
                <p>
                    5. We may collect the following Data, which includes personal Data, from
                    you:
                </p>
                <p>
                    a. name;
                </p>
                <p>
                    b. contact Information such as email addresses and telephone numbers;
                </p>
                <p>
                    c. financial information such as credit / debit card numbers;
                </p>
                <p>
                    d. IP address (automatically collected);
                </p>
                <p>
                    in each case, in accordance with this privacy policy.
                </p>
                <br />
                <p>
                    <strong>How we collect Data</strong>
                </p>
                <p>
                    6. We collect Data in the following ways:
                </p>
                <p>
                    a. data is given to us by you; and
                </p>
                <p>
                    b. data is collected automatically.
                </p>
                <br />
                <p>
                    <strong>Data that is given to us by you</strong>
                </p>
                <p>
                    7. R2SA Leads Limited will collect your Data in a number of ways, for
                    example:
                </p>
                <p>
                    a. when you contact us through the Website, by telephone, post, e-mail or
                    through any other means;
                </p>
                <p>
                    b. when you register with us and set up an account to receive our
                    products/services;
                </p>
                <p>
                    c. when you make payments to us, through this Website or otherwise;
                </p>
                <p>
                    d. when you elect to receive marketing communications from us;
                </p>
                <p>
                    e. when you use our services;
                </p>
                <p>
                    in each case, in accordance with this privacy policy.
                </p>
                <br />
                <p>
                    <strong>Data that is collected automatically</strong>
                </p>
                <p>
                    8. To the extent that you access the Website, we will collect your Data
                    automatically, for example:
                </p>
                <p>
                    a. we automatically collect some information about your visit to the
                    Website. This information helps us to make improvements to Website content
                    and navigation, and includes your IP address, the date, times and frequency
                    with which you access the Website and the way you use and interact with its
                    content.
                </p>
                <br />
                <p>
                    <strong>Our use of Data</strong>
                </p>
                <p>
                    9. Any or all of the above Data may be required by us from time to time in
                    order to provide you with the best possible service and experience when
                    using our Website. Specifically, Data may be used by us for the following
                    reasons:
                </p>
                <p>
                    a. internal record keeping;
                </p>
                <p>
                    b. improvement of our products / services;
                </p>
                <p>
                    in each case, in accordance with this privacy policy.
                </p>
                <p>
                    10. We may use your Data for the above purposes if we deem it necessary to
                    do so for our legitimate interests. If you are not satisfied with this, you
                    have the right to object in certain circumstances (see the section headed
                    "Your rights" below).
                </p>
                <p>
                    11. When you register with us and set up an account to receive our
                    services, the legal basis for this processing is the performance of a
                    contract between you and us and/or taking steps, at your request, to enter
                    into such a contract.
                </p>
                <br />
                <p>
                    <strong>Who we share Data with</strong>
                </p>
                <p>
                    12. We may share your Data with the following groups of people for the
                    following reasons:
                </p>
                <p>
                    a. any of our group companies or affiliates - to ensure the proper
                    administration of our website and business;
                </p>
                <p>
                    b. third party payment providers who process payments made over the Website
                    - to enable third party payment providers to process user payments and
                    refunds;
                </p>
                <p>
                    in each case, in accordance with this privacy policy.
                </p>
                <br />
                <p>
                    <strong>Keeping Data secure</strong>
                </p>
                <p>
                    13. We will use technical and organisational measures to safeguard your
                    Data, for example:
                </p>
                <p>
                    a. access to your account is controlled by a password and a user name that
                    is unique to you.
                </p>
                <p>
                    b. we store your Data on secure servers.
                </p>
                <p>
                    c. payment details are encrypted using SSL technology (typically you will
                    see a lock icon or green address bar (or both) in your browser when we use
                    this technology.
                </p>
                <p>
                    14. Technical and organisational measures include measures to deal with any
                    suspected data breach. If you suspect any misuse or loss or unauthorised
                    access to your Data, please let us know immediately by contacting us via
                    this e-mail address: oscar@sav-estates.co.uk.
                </p>
                <p>
                    15. If you want detailed information from Get Safe Online on how to protect
                    your information and your computers and devices against fraud, identity
                    theft, viruses and many other online problems, please visit
                    www.getsafeonline.org. Get Safe Online is supported by HM Government and
                    leading businesses.
                </p>
                <br />
                <p>
                    <strong>Data retention</strong>
                </p>
                <p>
                    16. Unless a longer retention period is required or permitted by law, we
                    will only hold your Data on our systems for the period necessary to fulfil
                    the purposes outlined in this privacy policy or until you request that the
                    Data be deleted.
                </p>
                <p>
                    17. Even if we delete your Data, it may persist on backup or archival media
                    for legal, tax or regulatory purposes.
                </p><br />
                <p>
                    <strong>Your rights</strong>
                </p>
                <p>
                    18. You have the following rights in relation to your Data:
                </p>
                <p>
                    a. <strong>Right to access</strong> - the right to request (i) copies of
                    the information we hold about you at any time, or (ii) that we modify,
                    update or delete such information. If we provide you with access to the
                    information we hold about you, we will not charge you for this, unless your
                    request is "manifestly unfounded or excessive." Where we are legally
                    permitted to do so, we may refuse your request. If we refuse your request,
                    we will tell you the reasons why.
                </p>
                <p>
                    b. <strong>Right to correct</strong> - the right to have your Data
                    rectified if it is inaccurate or incomplete.
                </p>
                <p>
                    c. <strong>Right to erase</strong> - the right to request that we delete or
                    remove your Data from our systems.
                </p>
                <p>
                    d. <strong>Right to restrict our use of your Data</strong> - the right to
                    "block" us from using your Data or limit the way in which we can use it.
                </p>
                <p>
                    e. <strong>Right to data portability</strong> - the right to request that
                    we move, copy or transfer your Data.
                </p>
                <p>
                    f. <strong>Right to object</strong> - the right to object to our use of
                    your Data including where we use it for our legitimate interests.
                </p>
                <p>
                    19. To make enquiries, exercise any of your rights set out above, or
                    withdraw your consent to the processing of your Data (where consent is our
                    legal basis for processing your Data), please contact us via this e-mail
                    address: oscar@sav-estates.co.uk.
                </p>
                <p>
                    20. If you are not satisfied with the way a complaint you make in relation
                    to your Data is handled by us, you may be able to refer your complaint to
                    the relevant data protection authority. For the UK, this is the Information
                    Commissioner's Office (ICO). The ICO's contact details can be found on
                    their website at https://ico.org.uk/.
                </p>
                <p>
                    21. It is important that the Data we hold about you is accurate and
                    current. Please keep us informed if your Data changes during the period for
                    which we hold it.
                </p>
                <br />
                <p>
                    <strong>
                        Transfers outside the United Kingdom and European Economic Area
                    </strong>
                    <strong></strong>
                </p>
                <p>
                    22. Data which we collect from you may be stored and processed in and
                    transferred to countries outside of the UK and European Economic Area
                    (EEA). For example, this could occur if our servers are located in a
                    country outside the UK or EEA or one of our service providers is situated
                    in a country outside the UK or EEA. We also share information with our
                    group companies, some of which are located outside the UK or EEA.
                </p>
                <p>
                    23. We will only transfer Data outside the UK or EEA where it is compliant
                    with data protection legislation and the means of transfer provides
                    adequate safeguards in relation to your data, eg by way of data transfer
                    agreement, incorporating the current standard contractual clauses adopted
                    by the European Commission.
                </p>
                <p>
                    24. To ensure that your Data receives an adequate level of protection, we
                    have put in place appropriate safeguards and procedures with the third
                    parties we share your Data with. This ensures your Data is treated by those
                    third parties in a way that is consistent with the Data Protection Laws.
                </p>
                <br />
                <p>
                    <strong>Links to other websites</strong>
                </p>
                <p>
                    25. This Website may, from time to time, provide links to other websites.
                    We have no control over such websites and are not responsible for the
                    content of these websites. This privacy policy does not extend to your use
                    of such websites. You are advised to read the privacy policy or statement
                    of other websites prior to using them.
                </p>
                <br />
                <p>
                    <strong>Changes of business ownership and control</strong>
                </p>
                <p>
                    26. R2SA Leads Limited may, from time to time, expand or reduce our
                    business and this may involve the sale and/or the transfer of control of
                    all or part of R2SA Leads Limited. Data provided by Users will, where it is
                    relevant to any part of our business so transferred, be transferred along
                    with that part and the new owner or newly controlling party will, under the
                    terms of this privacy policy, be permitted to use the Data for the purposes
                    for which it was originally supplied to us.
                </p>
                <p>
                    27. We may also disclose Data to a prospective purchaser of our business or
                    any part of it.
                </p>
                <p>
                    28. In the above instances, we will take steps with the aim of ensuring
                    your privacy is protected.
                </p>
                <br />
                <p>
                    <strong>General</strong>
                </p>
                <p>
                    29. You may not transfer any of your rights under this privacy policy to
                    any other person. We may transfer our rights under this privacy policy
                    where we reasonably believe your rights will not be affected.
                </p>
                <p>
                    30. If any court or competent authority finds that any provision of this
                    privacy policy (or part of any provision) is invalid, illegal or
                    unenforceable, that provision or part-provision will, to the extent
                    required, be deemed to be deleted, and the validity and enforceability of
                    the other provisions of this privacy policy will not be affected.
                </p>
                <p>
                    31. Unless otherwise agreed, no delay, act or omission by a party in
                    exercising any right or remedy will be deemed a waiver of that, or any
                    other, right or remedy.
                </p>
                <p>
                    32. This Agreement will be governed by and interpreted according to the law
                    of England and Wales. All disputes arising under the Agreement will be
                    subject to the exclusive jurisdiction of the English and Welsh courts.
                </p>
                <br />
                <p>
                    <strong>Changes to this privacy policy</strong>
                </p>
                <p>
                    33. R2SA Leads Limited reserves the right to change this privacy policy as
                    we may deem necessary from time to time or as may be required by law. Any
                    changes will be immediately posted on the Website and you are deemed to
                    have accepted the terms of the privacy policy on your first use of the
                    Website following the alterations.
                    <br/>
                    <br/>
                    You may contact R2SA Leads Limited by email at oscar@sav-estates.co.uk.
                </p>
                <br />
                <p>
                    <strong>Attribution</strong>
                </p>
                <p>
                34. This privacy policy was created using a document from    <a href="https://www.rocketlawyer.com/gb/en/">Rocket Lawyer</a>
                    (https://www.rocketlawyer.com/gb/en).
                </p>
                <p>
                    This privacy policy was created on <strong>15 January 2023</strong>.
                </p>
            </div>
        </div>
	)
}

export default PrivacyPolicy